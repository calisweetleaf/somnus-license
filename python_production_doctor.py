#!/usr/bin/env python3
"""
Python Production Doctor - Comprehensive Code Health Assessment Tool

Scans Python files/directories to identify:
- Syntax errors
- TODOs and technical debt markers
- Stub implementations (empty, pass, ellipsis, NotImplementedError)
- Simple placeholder returns (return None, 0, "", etc.)
- Incomplete method implementations
- Missing docstrings
- Suspiciously short functions
- Unimplemented abstract methods
- Type hint completeness
- Test coverage gaps

Outputs a detailed markdown report suitable for production readiness reviews.
"""

import ast
import tokenize
import io
import re
import sys
import os
import json
import datetime
import logging
import argparse
import concurrent.futures
import fnmatch
from dataclasses import dataclass, asdict
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set, Any, Union

# Default configuration
DEFAULT_CONFIG = {
    "min_function_lines": 5,
    "min_docstring_length": 15,
    "test_coverage_threshold": 0.7,
    "ignore_patterns": [
        "__pycache__/*",
        "*.pyc",
        ".git/*",
        ".venv/*",
        "venv/*",
        "env/*",
        "node_modules/*"
    ],
    "ignore_functions": [
        "__init__",
        "__str__",
        "__repr__"
    ],
    "severity_levels": {
        "syntax_errors": "critical",
        "unimplemented_abstracts": "critical",
        "stubs": "serious",
        "simple_returns": "serious",
        "incomplete_methods": "serious",
        "test_gaps": "serious",
        "todos": "minor",
        "missing_docstrings": "minor",
        "suspicious_short_functions": "minor",
        "type_hint_gaps": "minor"
    }
}

@dataclass
class DiagnosticIssue:
    """Single diagnostic issue"""
    category: str
    severity: str
    line_number: int
    message: str
    details: Dict[str, Any]

@dataclass
class DiagnosticResult:
    """Complete diagnostic result for a file"""
    file_path: str
    issues: List[DiagnosticIssue]
    metrics: Dict[str, int]
    code_map: Optional[Dict[str, Any]] = None

    def get_issues_by_severity(self, severity: str) -> List[DiagnosticIssue]:
        return [issue for issue in self.issues if issue.severity == severity]

    def get_issues_by_category(self, category: str) -> List[DiagnosticIssue]:
        return [issue for issue in self.issues if issue.category == category]

class KeyManager:
    """Manages the pool of ephemeral API keys from a file."""
    def __init__(self, key_file_path: str):
        self.key_file_path = key_file_path
        self.keys = self._load_keys()

    def _load_keys(self) -> List[str]:
        """Load keys from the key file."""
        if not os.path.exists(self.key_file_path):
            return []
        with open(self.key_file_path, 'r') as f:
            keys = [line.strip() for line in f if line.strip()]
        return keys

    def get_key(self) -> Optional[str]:
        """Get the next available key."""
        if not self.keys:
            return None
        return self.keys[0]

    def retire_key(self, key: str):
        """Retire a key and rewrite the key file."""
        if key in self.keys:
            self.keys.remove(key)
            with open(self.key_file_path, 'w') as f:
                for k in self.keys:
                    f.write(k + '\n')

class ConfigManager:
    """Manages configuration loading and validation"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = DEFAULT_CONFIG.copy()
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
        
        # Initialize KeyManager
        self.key_manager = KeyManager('openrouter_keys.txt')
        self.config['key_manager'] = self.key_manager

    
    def load_config(self, config_path: str):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            self._merge_config(user_config)
            logging.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            logging.warning(f"Failed to load config from {config_path}: {e}")
    
    def _merge_config(self, user_config: Dict[str, Any]):
        """Merge user config with defaults"""
        for key, value in user_config.items():
            if isinstance(value, dict) and key in self.config:
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

class ProductionDoctor:
    """Comprehensive Python code health diagnostic tool"""
    
    TODO_PATTERNS = [
        (r'\bTODO\b', 'Action Required'),
        (r'\bFIXME\b', 'Critical Fix Needed'),
        (r'\bHACK\b', 'Technical Debt'),
        (r'\bXXX\b', 'Urgent Review'),
        (r'\bNOTE\b', 'Important Note'),
        (r'\bTEMP\b', 'Temporary Code'),
        (r'\bWIP\b', 'Work In Progress')
    ]
    
    SIMPLE_RETURN_PATTERNS = [
        (r'^\s*return\s+None\s*$', 'None'),
        (r'^\s*return\s+0\s*$', 'Zero'),
        (r'^\s*return\s+""\s*$', 'Empty String'),
        (r"^\s*return\s+''\s*$", 'Empty String'),
        (r'^\s*return\s+\[\]\s*$', 'Empty List'),
        (r'^\s*return\s+\{\}\s*$', 'Empty Dict'),
        (r'^\s*return\s+False\s*$', 'False'),
        (r'^\s*return\s+True\s*$', 'True'),
        (r'^\s*return\s+-1\s*$', 'Negative One'),
    ]

    def __init__(self, file_path: str, config: 'ConfigManager', project_root: str):
        """
        Initialize ProductionDoctor for a specific file.
        
        Args:
            file_path: Absolute path to the Python file to analyze
            config: ConfigManager instance with analysis settings
            project_root: Root directory of the project for relative path calculations
        """
        self.file_path = file_path
        self.config = config
        self.project_root = project_root
        self.source_code: Optional[str] = None
        self.tree: Optional[ast.AST] = None
        self.lines: List[str] = []
        self.issues: List[DiagnosticIssue] = []
        self.metrics: Dict[str, int] = {
            'total_lines': 0,
            'total_functions': 0,
            'total_classes': 0,
            'documented_functions': 0,
            'type_hinted_functions': 0,
        }
        self._load_file()

    def _load_file(self) -> bool:
        """
        Load and parse the source file.
        
        Returns:
            True if file was loaded and parsed successfully, False otherwise
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
                self.source_code = f.read()
            self.lines = self.source_code.splitlines()
            self.metrics['total_lines'] = len(self.lines)
            return True
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_path}")
            return False
        except PermissionError:
            logging.error(f"Permission denied reading file: {self.file_path}")
            return False
        except Exception as e:
            logging.error(f"Error loading file {self.file_path}: {e}")
            return False

    def run_diagnostics(self) -> DiagnosticResult:
        """
        Run all diagnostic checks on the loaded file.
        
        Returns:
            DiagnosticResult containing all found issues and metrics
        """
        self.issues = []
        
        if not self.source_code:
            return DiagnosticResult(
                file_path=self.file_path,
                issues=self.issues,
                metrics=self.metrics
            )
        
        # Check for syntax errors first - if present, skip AST-based checks
        syntax_issues = self.check_syntax()
        self.issues.extend(syntax_issues)
        
        if syntax_issues:
            # Cannot perform AST analysis on files with syntax errors
            return DiagnosticResult(
                file_path=self.file_path,
                issues=self.issues,
                metrics=self.metrics
            )
        
        # Parse AST for further analysis
        try:
            self.tree = ast.parse(self.source_code, filename=self.file_path)
        except SyntaxError:
            # Already caught above, but handle edge cases
            return DiagnosticResult(
                file_path=self.file_path,
                issues=self.issues,
                metrics=self.metrics
            )
        
        # Run all diagnostic checks
        self.issues.extend(self.find_todos())
        self.issues.extend(self.find_stubs())
        self.issues.extend(self.find_simple_returns())
        self.issues.extend(self.find_incomplete_methods())
        self.issues.extend(self.find_missing_docstrings())
        self.issues.extend(self.find_suspicious_short_functions())
        self.issues.extend(self.find_unimplemented_abstracts())
        self.issues.extend(self.find_type_hint_gaps())
        self.issues.extend(self.find_test_gaps())
        
        return DiagnosticResult(
            file_path=self.file_path,
            issues=self.issues,
            metrics=self.metrics
        )

    def check_syntax(self) -> List[DiagnosticIssue]:
        """
        Check for Python syntax errors in the source file.
        
        Returns:
            List of DiagnosticIssue for any syntax errors found
        """
        issues = []
        try:
            ast.parse(self.source_code, filename=self.file_path)
        except SyntaxError as e:
            severity = self.config.get('severity_levels', {}).get('syntax_errors', 'critical')
            issues.append(DiagnosticIssue(
                category='syntax_errors',
                severity=severity,
                line_number=e.lineno or 0,
                message=f"SyntaxError: {e.msg}",
                details={
                    'error_type': 'SyntaxError',
                    'offset': e.offset,
                    'text': e.text.strip() if e.text else ''
                }
            ))
        except Exception as e:
            issues.append(DiagnosticIssue(
                category='syntax_errors',
                severity='critical',
                line_number=0,
                message=f"Parse error: {str(e)}",
                details={'error_type': type(e).__name__}
            ))
        return issues

    def find_todos(self) -> List[DiagnosticIssue]:
        """
        Find TODO, FIXME, HACK, and other technical debt markers in comments.
        
        Returns:
            List of DiagnosticIssue for each marker found
        """
        issues = []
        severity = self.config.get('severity_levels', {}).get('todos', 'minor')
        
        try:
            tokens = list(tokenize.generate_tokens(io.StringIO(self.source_code).readline))
            for token in tokens:
                if token.type == tokenize.COMMENT:
                    comment_text = token.string
                    line_number = token.start[0]
                    
                    for pattern, marker_type in self.TODO_PATTERNS:
                        if re.search(pattern, comment_text, re.IGNORECASE):
                            # Extract the actual comment content
                            clean_comment = comment_text.lstrip('#').strip()
                            issues.append(DiagnosticIssue(
                                category='todos',
                                severity=severity,
                                line_number=line_number,
                                message=clean_comment[:100],  # Truncate long comments
                                details={
                                    'marker_type': marker_type,
                                    'full_comment': clean_comment
                                }
                            ))
                            break  # Only report once per comment
        except tokenize.TokenError as e:
            logging.debug(f"Tokenize error in {self.file_path}: {e}")
        except Exception as e:
            logging.debug(f"Error finding TODOs in {self.file_path}: {e}")
        
        return issues

    def find_stubs(self) -> List[DiagnosticIssue]:
        """
        Find stub implementations: pass, ellipsis (...), or NotImplementedError.
        
        Returns:
            List of DiagnosticIssue for each stub found
        """
        issues = []
        severity = self.config.get('severity_levels', {}).get('stubs', 'serious')
        ignore_functions = self.config.get('ignore_functions', [])
        
        if not self.tree:
            return issues
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = node.name
                
                # Skip ignored functions
                if func_name in ignore_functions:
                    continue
                
                # Get the function body excluding docstring
                body = node.body
                if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                    if isinstance(body[0].value.value, str):
                        body = body[1:]  # Skip docstring
                
                if not body:
                    continue
                
                stub_type = None
                
                # Check for single-statement stubs
                if len(body) == 1:
                    stmt = body[0]
                    
                    # Check for 'pass'
                    if isinstance(stmt, ast.Pass):
                        stub_type = 'pass statement'
                    
                    # Check for ellipsis '...'
                    elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                        if stmt.value.value is ...:
                            stub_type = 'ellipsis (...)'
                    
                    # Check for 'raise NotImplementedError'
                    elif isinstance(stmt, ast.Raise):
                        if stmt.exc:
                            if isinstance(stmt.exc, ast.Call):
                                if isinstance(stmt.exc.func, ast.Name):
                                    if stmt.exc.func.id == 'NotImplementedError':
                                        stub_type = 'NotImplementedError'
                            elif isinstance(stmt.exc, ast.Name):
                                if stmt.exc.id == 'NotImplementedError':
                                    stub_type = 'NotImplementedError'
                
                if stub_type:
                    issues.append(DiagnosticIssue(
                        category='stubs',
                        severity=severity,
                        line_number=node.lineno,
                        message=f"Stub implementation in {func_name}()",
                        details={
                            'function_name': func_name,
                            'stub_type': stub_type
                        }
                    ))
        
        return issues

    def find_simple_returns(self) -> List[DiagnosticIssue]:
        """
        Find functions that only return simple placeholder values.
        
        Returns:
            List of DiagnosticIssue for each placeholder return found
        """
        issues = []
        severity = self.config.get('severity_levels', {}).get('simple_returns', 'serious')
        ignore_functions = self.config.get('ignore_functions', [])
        
        if not self.tree:
            return issues
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = node.name
                
                if func_name in ignore_functions:
                    continue
                
                # Get function body excluding docstring
                body = node.body
                if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                    if isinstance(body[0].value.value, str):
                        body = body[1:]
                
                # Check if function only has a simple return
                if len(body) == 1 and isinstance(body[0], ast.Return):
                    return_stmt = body[0]
                    return_value = return_stmt.value
                    return_type = None
                    
                    if return_value is None:
                        return_type = 'None (implicit)'
                    elif isinstance(return_value, ast.Constant):
                        val = return_value.value
                        if val is None:
                            return_type = 'None'
                        elif val == 0:
                            return_type = 'Zero'
                        elif val == '':
                            return_type = 'Empty String'
                        elif val is False:
                            return_type = 'False'
                        elif val is True:
                            return_type = 'True'
                        elif val == -1:
                            return_type = 'Negative One'
                    elif isinstance(return_value, ast.List) and len(return_value.elts) == 0:
                        return_type = 'Empty List'
                    elif isinstance(return_value, ast.Dict) and len(return_value.keys) == 0:
                        return_type = 'Empty Dict'
                    elif isinstance(return_value, ast.Tuple) and len(return_value.elts) == 0:
                        return_type = 'Empty Tuple'
                    elif isinstance(return_value, ast.Set) and len(return_value.elts) == 0:
                        return_type = 'Empty Set'
                    
                    if return_type:
                        issues.append(DiagnosticIssue(
                            category='simple_returns',
                            severity=severity,
                            line_number=return_stmt.lineno,
                            message=f"Placeholder return in {func_name}()",
                            details={
                                'function_name': func_name,
                                'return_type': return_type
                            }
                        ))
        
        return issues

    def find_incomplete_methods(self) -> List[DiagnosticIssue]:
        """
        Find class methods that appear incomplete (very short body after docstring).
        
        Returns:
            List of DiagnosticIssue for each incomplete method found
        """
        issues = []
        severity = self.config.get('severity_levels', {}).get('incomplete_methods', 'serious')
        ignore_functions = self.config.get('ignore_functions', [])
        
        if not self.tree:
            return issues
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_name = item.name
                        
                        if method_name in ignore_functions:
                            continue
                        
                        # Get body excluding docstring
                        body = item.body
                        has_docstring = False
                        if body and isinstance(body[0], ast.Expr):
                            if isinstance(body[0].value, ast.Constant):
                                if isinstance(body[0].value.value, str):
                                    has_docstring = True
                                    body = body[1:]
                        
                        # Method with only docstring and single trivial statement
                        if has_docstring and len(body) == 1:
                            stmt = body[0]
                            is_incomplete = False
                            
                            # Single pass after docstring
                            if isinstance(stmt, ast.Pass):
                                is_incomplete = True
                            # Single return None/simple value after docstring
                            elif isinstance(stmt, ast.Return):
                                if stmt.value is None:
                                    is_incomplete = True
                                elif isinstance(stmt.value, ast.Constant):
                                    if stmt.value.value in (None, 0, '', False, [], {}):
                                        is_incomplete = True
                            # Single expression that's just ellipsis
                            elif isinstance(stmt, ast.Expr):
                                if isinstance(stmt.value, ast.Constant):
                                    if stmt.value.value is ...:
                                        is_incomplete = True
                            
                            if is_incomplete:
                                issues.append(DiagnosticIssue(
                                    category='incomplete_methods',
                                    severity=severity,
                                    line_number=item.lineno,
                                    message=f"Incomplete method {class_name}.{method_name}()",
                                    details={
                                        'class_name': class_name,
                                        'method_name': method_name
                                    }
                                ))
        
        return issues

    def find_missing_docstrings(self) -> List[DiagnosticIssue]:
        """
        Find functions and classes without docstrings.
        
        Returns:
            List of DiagnosticIssue for each missing docstring
        """
        issues = []
        severity = self.config.get('severity_levels', {}).get('missing_docstrings', 'minor')
        ignore_functions = self.config.get('ignore_functions', [])
        min_docstring_length = self.config.get('min_docstring_length', 15)
        
        if not self.tree:
            return issues
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                if not docstring or len(docstring.strip()) < min_docstring_length:
                    issues.append(DiagnosticIssue(
                        category='missing_docstrings',
                        severity=severity,
                        line_number=node.lineno,
                        message=f"Missing or short docstring for class {node.name}",
                        details={
                            'entity_type': 'class',
                            'entity_name': node.name
                        }
                    ))
                self.metrics['total_classes'] = self.metrics.get('total_classes', 0) + 1
            
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = node.name
                
                if func_name in ignore_functions:
                    continue
                
                # Skip nested functions for docstring checks
                if func_name.startswith('_') and not func_name.startswith('__'):
                    # Still count but don't require docstrings for private functions
                    self.metrics['total_functions'] = self.metrics.get('total_functions', 0) + 1
                    continue
                
                self.metrics['total_functions'] = self.metrics.get('total_functions', 0) + 1
                
                docstring = ast.get_docstring(node)
                if docstring and len(docstring.strip()) >= min_docstring_length:
                    self.metrics['documented_functions'] = self.metrics.get('documented_functions', 0) + 1
                else:
                    issues.append(DiagnosticIssue(
                        category='missing_docstrings',
                        severity=severity,
                        line_number=node.lineno,
                        message=f"Missing or short docstring for function {func_name}()",
                        details={
                            'entity_type': 'function',
                            'entity_name': func_name
                        }
                    ))
        
        return issues

    def find_suspicious_short_functions(self) -> List[DiagnosticIssue]:
        """
        Find functions that are suspiciously short (may be incomplete).
        
        Returns:
            List of DiagnosticIssue for each short function found
        """
        issues = []
        severity = self.config.get('severity_levels', {}).get('suspicious_short_functions', 'minor')
        ignore_functions = self.config.get('ignore_functions', [])
        min_function_lines = self.config.get('min_function_lines', 5)
        
        if not self.tree:
            return issues
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = node.name
                
                if func_name in ignore_functions:
                    continue
                
                # Skip dunder methods and property getters/setters
                if func_name.startswith('__') and func_name.endswith('__'):
                    continue
                
                # Calculate function length
                if hasattr(node, 'end_lineno') and node.end_lineno:
                    func_lines = node.end_lineno - node.lineno + 1
                else:
                    # Fallback: count body statements
                    func_lines = len(node.body)
                
                # Exclude docstring from line count
                body = node.body
                if body and isinstance(body[0], ast.Expr):
                    if isinstance(body[0].value, ast.Constant):
                        if isinstance(body[0].value.value, str):
                            # Subtract approximate docstring lines
                            doc = body[0].value.value
                            func_lines -= doc.count('\n') + 1
                
                if func_lines < min_function_lines and len(node.body) > 0:
                    # Skip if it's a known pattern (property, simple wrapper)
                    if len(node.decorator_list) > 0:
                        decorator_names = []
                        for dec in node.decorator_list:
                            if isinstance(dec, ast.Name):
                                decorator_names.append(dec.id)
                            elif isinstance(dec, ast.Attribute):
                                decorator_names.append(dec.attr)
                        if any(d in ['property', 'setter', 'getter', 'staticmethod', 'classmethod'] 
                               for d in decorator_names):
                            continue
                    
                    issues.append(DiagnosticIssue(
                        category='suspicious_short_functions',
                        severity=severity,
                        line_number=node.lineno,
                        message=f"Function {func_name}() is suspiciously short",
                        details={
                            'function_name': func_name,
                            'line_count': max(1, func_lines)
                        }
                    ))
        
        return issues

    def find_unimplemented_abstracts(self) -> List[DiagnosticIssue]:
        """
        Find abstract methods that have stub implementations in subclasses.
        
        Returns:
            List of DiagnosticIssue for each unimplemented abstract method
        """
        issues = []
        severity = self.config.get('severity_levels', {}).get('unimplemented_abstracts', 'critical')
        
        if not self.tree:
            return issues
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                # Check if class inherits from ABC or has ABCMeta
                is_abstract_class = False
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id in ('ABC', 'ABCMeta'):
                        is_abstract_class = True
                        break
                    if isinstance(base, ast.Attribute) and base.attr in ('ABC', 'ABCMeta'):
                        is_abstract_class = True
                        break
                
                # Check for ABCMeta in metaclass
                for keyword in node.keywords:
                    if keyword.arg == 'metaclass':
                        if isinstance(keyword.value, ast.Name):
                            if keyword.value.id == 'ABCMeta':
                                is_abstract_class = True
                
                if not is_abstract_class:
                    continue
                
                # Find abstract methods with stub bodies
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        is_abstract = False
                        for decorator in item.decorator_list:
                            if isinstance(decorator, ast.Name):
                                if decorator.id in ('abstractmethod', 'abstractproperty'):
                                    is_abstract = True
                            elif isinstance(decorator, ast.Attribute):
                                if decorator.attr in ('abstractmethod', 'abstractproperty'):
                                    is_abstract = True
                        
                        if is_abstract:
                            # Check if body is just pass/... (acceptable for abstract)
                            # But flag if there's supposed implementation that's stubbed
                            body = item.body
                            if body and isinstance(body[0], ast.Expr):
                                if isinstance(body[0].value, ast.Constant):
                                    if isinstance(body[0].value.value, str):
                                        body = body[1:]
                            
                            # Abstract methods with pass/... are OK, but log for awareness
                            if len(body) == 1:
                                stmt = body[0]
                                if isinstance(stmt, ast.Raise):
                                    if stmt.exc and isinstance(stmt.exc, ast.Call):
                                        if isinstance(stmt.exc.func, ast.Name):
                                            if stmt.exc.func.id == 'NotImplementedError':
                                                # This is actually proper abstract method pattern
                                                continue
                            
                            # If not proper pattern, might be incomplete
                            has_real_implementation = False
                            for stmt in body:
                                if not isinstance(stmt, (ast.Pass, ast.Expr)):
                                    if isinstance(stmt, ast.Return):
                                        if stmt.value is not None:
                                            has_real_implementation = True
                                    else:
                                        has_real_implementation = True
                            
                            if not has_real_implementation and body:
                                issues.append(DiagnosticIssue(
                                    category='unimplemented_abstracts',
                                    severity=severity,
                                    line_number=item.lineno,
                                    message=f"Abstract method {node.name}.{item.name}() has no implementation",
                                    details={
                                        'class_name': node.name,
                                        'method_name': item.name
                                    }
                                ))
        
        return issues

    def find_type_hint_gaps(self) -> List[DiagnosticIssue]:
        """
        Find functions missing type hints on parameters or return values.
        
        Returns:
            List of DiagnosticIssue for each function with incomplete type hints
        """
        issues = []
        severity = self.config.get('severity_levels', {}).get('type_hint_gaps', 'minor')
        ignore_functions = self.config.get('ignore_functions', [])
        
        if not self.tree:
            return issues
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = node.name
                
                if func_name in ignore_functions:
                    continue
                
                missing_hints = []
                
                # Check return type
                if node.returns is None:
                    missing_hints.append('return type')
                
                # Check parameters (skip 'self' and 'cls')
                for arg in node.args.args:
                    if arg.arg in ('self', 'cls'):
                        continue
                    if arg.annotation is None:
                        missing_hints.append(f"param '{arg.arg}'")
                
                # Check *args and **kwargs
                if node.args.vararg and node.args.vararg.annotation is None:
                    missing_hints.append('*args')
                if node.args.kwarg and node.args.kwarg.annotation is None:
                    missing_hints.append('**kwargs')
                
                # Check keyword-only args
                for arg in node.args.kwonlyargs:
                    if arg.annotation is None:
                        missing_hints.append(f"param '{arg.arg}'")
                
                if missing_hints:
                    # Track for metrics
                    pass
                else:
                    self.metrics['type_hinted_functions'] = self.metrics.get('type_hinted_functions', 0) + 1
                
                # Only report if function has some hints but is incomplete
                # (to avoid flooding on legacy codebases)
                has_any_hints = (node.returns is not None or 
                                any(arg.annotation is not None for arg in node.args.args 
                                    if arg.arg not in ('self', 'cls')))
                
                if has_any_hints and missing_hints:
                    issues.append(DiagnosticIssue(
                        category='type_hint_gaps',
                        severity=severity,
                        line_number=node.lineno,
                        message=f"Incomplete type hints in {func_name}()",
                        details={
                            'function_name': func_name,
                            'missing_hints': ', '.join(missing_hints[:5])  # Limit to 5
                        }
                    ))
        
        return issues

    def find_test_gaps(self) -> List[DiagnosticIssue]:
        """
        Check if this module has corresponding test files.
        
        Returns:
            List of DiagnosticIssue if test coverage appears lacking
        """
        issues = []
        severity = self.config.get('severity_levels', {}).get('test_gaps', 'serious')
        
        # Skip test files themselves
        file_name = os.path.basename(self.file_path)
        if file_name.startswith('test_') or file_name.endswith('_test.py'):
            return issues
        
        # Skip __init__.py and setup files
        if file_name in ('__init__.py', 'setup.py', 'conftest.py'):
            return issues
        
        # Look for corresponding test file
        module_name = file_name.replace('.py', '')
        possible_test_names = [
            f"test_{module_name}.py",
            f"{module_name}_test.py",
            f"tests/test_{module_name}.py",
            f"test/test_{module_name}.py",
        ]
        
        test_found = False
        search_dirs = [
            os.path.dirname(self.file_path),
            self.project_root,
            os.path.join(self.project_root, 'tests'),
            os.path.join(self.project_root, 'test'),
        ]
        
        for search_dir in search_dirs:
            if not os.path.isdir(search_dir):
                continue
            for test_name in possible_test_names:
                test_path = os.path.join(search_dir, os.path.basename(test_name))
                if os.path.exists(test_path):
                    test_found = True
                    break
            if test_found:
                break
        
        if not test_found:
            # Count functions to determine if tests should exist
            func_count = 0
            if self.tree:
                for node in ast.walk(self.tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if not node.name.startswith('_'):
                            func_count += 1
            
            # Only flag if there are public functions worth testing
            if func_count >= 2:
                rel_path = os.path.relpath(self.file_path, self.project_root)
                issues.append(DiagnosticIssue(
                    category='test_gaps',
                    severity=severity,
                    line_number=1,
                    message=f"No test file found for {module_name} ({func_count} public functions)",
                    details={
                        'module_path': rel_path,
                        'module_name': module_name,
                        'public_function_count': func_count
                    }
                ))
        
        return issues

    @staticmethod
    def generate_json_report(results: List[DiagnosticResult], project_root: str) -> str:
        """Generate JSON report for CI/CD integration"""
        report_data = {
            "project_root": project_root,
            "scan_date": datetime.datetime.now().isoformat(),
            "python_version": sys.version.split()[0],
            "summary": {},
            "files": []
        }
        
        # Calculate summary
        total_issues = 0
        severity_counts = defaultdict(int)
        category_counts = defaultdict(int)
        
        for result in results:
            file_data = {
                "file_path": os.path.relpath(result.file_path, project_root),
                "metrics": result.metrics,
                "issues": [asdict(issue) for issue in result.issues]
            }
            report_data["files"].append(file_data)
            
            total_issues += len(result.issues)
            for issue in result.issues:
                severity_counts[issue.severity] += 1
                category_counts[issue.category] += 1
        
        report_data["summary"] = {
            "total_issues": total_issues,
            "severity_counts": dict(severity_counts),
            "category_counts": dict(category_counts)
        }
        
        return json.dumps(report_data, indent=2)

    @staticmethod
    def generate_markdown_report(results: List[DiagnosticResult], project_root: str) -> str:
        """Generate enhanced markdown report"""
        report = [
            "# 🩺 Python Production Doctor Report\n",
            f"**Project Root:** `{project_root}`",
            f"**Scan Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Python Version:** {sys.version.split()[0]}",
            "\n---\n"
        ]
        
        # Enhanced summary with metrics
        total_issues = sum(len(result.issues) for result in results)
        total_files = len(results)
        
        # Calculate category counts for action plan
        category_counts = defaultdict(int)
        for result in results:
            for issue in result.issues:
                category_counts[issue.category] += 1
        
        if total_issues == 0:
            report.append("✅ **FULLY PRODUCTION READY** - No issues found!\n")
        else:
            # Categorize by severity
            critical = sum(len([i for i in result.issues if i.severity == 'critical']) for result in results)
            serious = sum(len([i for i in result.issues if i.severity == 'serious']) for result in results)
            minor = sum(len([i for i in result.issues if i.severity == 'minor']) for result in results)
            
            if critical > 0:
                status = "🔴 **CRITICAL ISSUES** - Cannot deploy"
            elif serious > 0:
                status = "🟠 **SERIOUS ISSUES** - Requires significant work"
            else:
                status = "🟡 **MINOR ISSUES** - Ready with minor fixes"
            
            report.append(f"{status}\n")
            report.append(f"**Files Scanned:** {total_files} | **Total Issues:** {total_issues}")
            report.append(f"- 🔴 Critical: {critical}")
            report.append(f"- 🟠 Serious: {serious}")  
            report.append(f"- 🟡 Minor: {minor}\n")
        
        # Add code quality metrics
        total_functions = sum(result.metrics.get('total_functions', 0) for result in results)
        documented_functions = sum(result.metrics.get('documented_functions', 0) for result in results)
        type_hinted_functions = sum(result.metrics.get('type_hinted_functions', 0) for result in results)
        
        if total_functions > 0:
            doc_coverage = (documented_functions / total_functions) * 100
            type_coverage = (type_hinted_functions / total_functions) * 100
            
            report.append("## 📈 Code Quality Metrics\n")
            report.append(f"- **Documentation Coverage:** {doc_coverage:.1f}% ({documented_functions}/{total_functions})")
            report.append(f"- **Type Hint Coverage:** {type_coverage:.1f}% ({type_hinted_functions}/{total_functions})\n")
        
        # File-by-file breakdown
        report.append("## 📁 File Analysis\n")
        
        for result in results:
            rel_path = os.path.relpath(result.file_path, project_root)
            total = len(result.issues)
            
            if total == 0:
                report.append(f"### ✅ `{rel_path}`\n")
                report.append("_No issues found - ready for production_\n")
                continue
                
            report.append(f"### 📄 `{rel_path}`\n")
            report.append(f"**Total Issues:** {total}\n")
            
            # Syntax errors
            syntax_errors = [i for i in result.issues if i.category == 'syntax_errors']
            if syntax_errors:
                report.append("#### ⚠️ Syntax Errors")
                for i, err in enumerate(syntax_errors, 1):
                    report.append(f"{i}. `{err.message}` (line {err.line_number})")
                report.append("")
            
            # TODOs
            todos = [i for i in result.issues if i.category == 'todos']
            if todos:
                report.append("#### 📝 Technical Debt")
                for i, issue in enumerate(todos, 1):
                    report.append(f"{i}. **{issue.severity}** at line {issue.line_number}: `{issue.message}`")
                report.append("")
            
            # Stubs
            stubs = [i for i in result.issues if i.category == 'stubs']
            if stubs:
                report.append("#### 🚧 Stub Implementations")
                for i, issue in enumerate(stubs, 1):
                    report.append(f"{i}. `{issue.details['function_name']}()` at line {issue.line_number} - **{issue.details['stub_type']}**")
                report.append("")
            
            # Simple returns
            simple_returns = [i for i in result.issues if i.category == 'simple_returns']
            if simple_returns:
                report.append("#### ⚠️ Placeholder Returns")
                for i, issue in enumerate(simple_returns, 1):
                    report.append(f"{i}. `{issue.details['function_name']}()` at line {issue.line_number} - returns **{issue.details['return_type']}**")
                report.append("")
            
            # Incomplete methods
            incomplete_methods = [i for i in result.issues if i.category == 'incomplete_methods']
            if incomplete_methods:
                report.append("#### 🧩 Incomplete Methods")
                for i, issue in enumerate(incomplete_methods, 1):
                    report.append(f"{i}. `{issue.details['class_name']}.{issue.details['method_name']}()` at line {issue.line_number}")
                report.append("")
            
            # Missing docstrings
            missing_docstrings = [i for i in result.issues if i.category == 'missing_docstrings']
            if missing_docstrings:
                report.append("#### 📚 Missing Docstrings")
                for i, issue in enumerate(missing_docstrings, 1):
                    report.append(f"{i}. {issue.details['entity_type'].capitalize()} `{issue.details['entity_name']}` at line {issue.line_number}")
                report.append("")
            
            # Suspicious short functions
            suspicious_short_functions = [i for i in result.issues if i.category == 'suspicious_short_functions']
            if suspicious_short_functions:
                report.append("#### 📏 Suspiciously Short Functions")
                for i, issue in enumerate(suspicious_short_functions, 1):
                    report.append(f"{i}. `{issue.details['function_name']}()` at line {issue.line_number} - only {issue.details['line_count']} line{'s' if issue.details['line_count'] > 1 else ''} of code")
                report.append("")
            
            # Unimplemented abstracts
            unimplemented_abstracts = [i for i in result.issues if i.category == 'unimplemented_abstracts']
            if unimplemented_abstracts:
                report.append("#### ❌ Unimplemented Abstract Methods")
                for i, issue in enumerate(unimplemented_abstracts, 1):
                    report.append(f"{i}. `{issue.details['class_name']}.{issue.details['method_name']}()` at line {issue.line_number}")
                report.append("")
            
            # Type hint gaps
            type_hint_gaps = [i for i in result.issues if i.category == 'type_hint_gaps']
            if type_hint_gaps:
                report.append("#### 🔍 Incomplete Type Hints")
                for i, issue in enumerate(type_hint_gaps, 1):
                    report.append(f"{i}. `{issue.details['function_name']}()` at line {issue.line_number} - missing: {issue.details['missing_hints']}")
                report.append("")
            
            # Test gaps
            test_gaps = [i for i in result.issues if i.category == 'test_gaps']
            if test_gaps:
                report.append("#### 🧪 Test Coverage Gaps")
                for i, issue in enumerate(test_gaps, 1):
                    report.append(f"{i}. `{issue.details['module_path']}` - {issue.message}")
                report.append("")
        
        # Action plan
        report.append("## 🚀 Recommended Action Plan\n")
        report.append("### Critical Fixes (Block Deployment)")
        if category_counts['syntax_errors'] > 0:
            report.append("- Fix all syntax errors")
        if category_counts['unimplemented_abstracts'] > 0:
            report.append("- Implement all abstract methods")
        
        report.append("\n### Serious Fixes (Required Before Release)")
        if category_counts['stubs'] > 0:
            report.append("- Replace all stub implementations with real code")
        if category_counts['simple_returns'] > 0:
            report.append("- Replace placeholder return values with real implementations")
        if category_counts['incomplete_methods'] > 0:
            report.append("- Complete all incomplete methods")
        if category_counts['test_gaps'] > 0:
            report.append("- Increase test coverage to at least 80%")
        
        report.append("\n### Quality Improvements (Recommended)")
        if category_counts['todos'] > 0:
            report.append("- Address all TODOs and technical debt")
        if category_counts['missing_docstrings'] > 0:
            report.append("- Add meaningful docstrings to all functions/classes")
        if category_counts['suspicious_short_functions'] > 0:
            report.append("- Review suspiciously short functions for completeness")
        if category_counts['type_hint_gaps'] > 0:
            report.append("- Complete all type hints for better maintainability")
        
        report.append("\n---\n")
        report.append("_This report generated by [Python Production Doctor](https://github.com/yourusername/production-doctor)_")
        
        return "\n".join(report)

def scan_project(project_root: str) -> List[DiagnosticResult]:
    """Scan entire project for production readiness"""
    results = []
    doctor = None
    
    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith('.py') and not file.startswith('test_'):
                file_path = os.path.join(root, file)
                print(f"Scanning: {os.path.relpath(file_path, project_root)}")
                doctor = ProductionDoctor(file_path, project_root)
                results.append(doctor.run_diagnostics())
    
    return results

def scan_project_parallel(project_root: str, config: ConfigManager, max_workers: int = 4) -> List[DiagnosticResult]:
    """Scan project with parallel processing"""
    python_files = []
    
    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                python_files.append(file_path)
    
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(analyze_file, file_path, config, project_root): file_path 
            for file_path in python_files
        }
        
        # Collect results
        for future in concurrent.futures.as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                result = future.result()
                if result:  # Only add non-empty results
                    results.append(result)
                    print(f"✅ {os.path.relpath(file_path, project_root)}")
            except Exception as e:
                print(f"❌ {os.path.relpath(file_path, project_root)}: {e}")
                logging.error(f"Failed to analyze {file_path}: {e}")
    
    return results

def analyze_file(file_path: str, config: ConfigManager, project_root: str) -> Optional[DiagnosticResult]:
    """Analyze a single file (for parallel processing)"""
    doctor = ProductionDoctor(file_path, config, project_root)
    result = doctor.run_diagnostics()
    
    # Only return results with issues or if file was successfully processed
    if result.issues or result.metrics['total_lines'] > 0:
        return result
    return None

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('production_doctor.log'),
            logging.StreamHandler(sys.stdout) if verbose else logging.NullHandler()
        ]
    )

def main():
    parser = argparse.ArgumentParser(description='Python Production Doctor - Code Health Assessment')
    parser.add_argument('project_root', help='Project root directory to scan')
    parser.add_argument('-o', '--output', default='production_report.md', 
                       help='Output file name (default: production_report.md)')
    parser.add_argument('-c', '--config', help='Configuration file path')
    parser.add_argument('-f', '--format', choices=['markdown', 'json'], default='markdown',
                       help='Output format (default: markdown)')
    parser.add_argument('-j', '--jobs', type=int, default=4,
                       help='Number of parallel jobs (default: 4)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Load configuration
    config = ConfigManager(args.config)
    
    project_root = os.path.abspath(args.project_root)
    
    print(f"🔍 Starting production readiness scan for {project_root}")
    print(f"📊 Using {args.jobs} parallel workers")
    
    # Scan project
    results = scan_project_parallel(project_root, config, args.jobs)
    
    print(f"\n📊 Generating {args.format} report...")
    
    # Generate report
    if args.format == 'json':
        report = ProductionDoctor.generate_json_report(results, project_root)
        if not args.output.endswith('.json'):
            args.output = args.output.replace('.md', '.json')
    else:
        report = ProductionDoctor.generate_markdown_report(results, project_root)
    
    # Write report
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ Report generated: {os.path.abspath(args.output)}")
    
    # Print summary
    total_issues = sum(len(result.issues) for result in results)
    critical_issues = sum(len([i for i in result.issues if i.severity == 'critical']) for result in results)
    
    print(f"\n📊 Summary: {len(results)} files scanned, {total_issues} issues found")
    if critical_issues > 0:
        print(f"🔴 {critical_issues} critical issues found - deployment blocked")
        sys.exit(1)
    elif total_issues == 0:
        print("🎉 Project is production ready!")
    else:
        print("⚠️  Project has issues but can proceed with caution")

if __name__ == "__main__":
    main()
