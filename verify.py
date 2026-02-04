"""
Verification script to check project completeness
Run this to verify all components are in place
"""

import os
import sys

# Project structure verification
REQUIRED_FILES = {
    'config.py': 'Configuration file',
    'requirements.txt': 'Python dependencies',
    '.env.example': 'Environment template',
    'README.md': 'Main documentation',
    'PROJECT_GUIDE.md': 'Usage guide',
    'pytest.ini': 'Test configuration',
}

REQUIRED_DIRS = {
    'agents': ['__init__.py', 'orchestrator.py'],
    'api': ['__init__.py', 'main.py'],
    'api/routes': ['__init__.py', 'health.py', 'knowledge.py', 'patients.py', 'query.py', 'recommendations.py'],
    'kb': ['__init__.py', 'vector_store.py', 'knowledge_base.py'],
    'models': ['__init__.py', 'patient.py', 'disease.py', 'treatment.py', 'metric.py', 'query.py'],
    'data': ['sample_knowledge.py'],
    'scripts': ['init_kb.py', 'start_server.py'],
    'tests': ['test_models.py', 'test_kb.py'],
}

def check_file_exists(filepath):
    """Check if a file exists"""
    return os.path.exists(filepath)

def verify_project():
    """Verify project completeness"""
    print("=" * 60)
    print("VERIFICATION: Agent慢病管理知识库")
    print("=" * 60)
    
    all_ok = True
    
    # Check root files
    print("\nRoot Files:")
    for file, desc in REQUIRED_FILES.items():
        exists = check_file_exists(file)
        status = "OK" if exists else "MISSING"
        print(f"  [{status}] {file} - {desc}")
        if not exists:
            all_ok = False
    
    # Check directories and their files
    print("\nDirectory Structure:")
    for dir_name, files in REQUIRED_DIRS.items():
        print(f"\n  [{dir_name}/]")
        for file in files:
            filepath = os.path.join(dir_name, file)
            exists = check_file_exists(filepath)
            status = "OK" if exists else "MISSING"
            print(f"    [{status}] {file}")
            if not exists:
                all_ok = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("VERIFICATION PASSED: All components are present!")
        print("=" * 60)
        print("\nProject Statistics:")
        
        # Count files
        py_files = []
        for root, dirs, files in os.walk('.'):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.endswith('.py'):
                    py_files.append(os.path.join(root, file))
        
        print(f"  - Python files: {len(py_files)}")
        print(f"  - Core modules: {len(REQUIRED_DIRS)}")
        print(f"  - Total lines of code: ~{len(py_files) * 150} (estimated)")
        
        print("\nReady to use!")
        print("\nNext steps:")
        print("  1. pip install -r requirements.txt")
        print("  2. cp .env.example .env  # Edit with your API keys")
        print("  3. python scripts/init_kb.py")
        print("  4. python scripts/start_server.py")
        
        return True
    else:
        print("VERIFICATION FAILED: Some components are missing")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = verify_project()
    sys.exit(0 if success else 1)