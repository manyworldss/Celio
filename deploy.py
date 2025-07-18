#!/usr/bin/env python3
"""
Fly.io Deployment Helper Script for Celio

This script helps prepare and deploy the Celio application to Fly.io.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_flyctl():
    """Check if flyctl is installed."""
    try:
        subprocess.run(['flyctl', 'version'], check=True, capture_output=True)
        print("✅ flyctl is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ flyctl not found. Install from: https://fly.io/docs/hands-on/install-flyctl/")
        return False

def check_requirements():
    """Check if all required files exist."""
    required_files = [
        'fly.toml',
        'Dockerfile',
        'requirements.txt',
        'celio/wsgi.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def run_tests():
    """Run basic Django checks."""
    print("🧪 Running Django checks...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'check'], check=True)
        print("✅ Django checks passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Django checks failed: {e}")
        return False

def deploy_to_fly():
    """Deploy to Fly.io."""
    print("🚀 Deploying to Fly.io...")
    try:
        subprocess.run(['flyctl', 'deploy'], check=True)
        print("✅ Deployment successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

def main():
    """Main deployment process."""
    print("🔧 Celio Fly.io Deployment Helper")
    print("=" * 40)
    
    # Check flyctl
    if not check_flyctl():
        return
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please fix missing files before deploying.")
        return
    
    # Run tests
    if not run_tests():
        print("\n❌ Tests failed.")
        return
    
    # Ask for deployment confirmation
    deploy = input("\n🚀 Ready to deploy to Fly.io? (y/N): ").lower().strip()
    if deploy == 'y':
        deploy_to_fly()
    else:
        print("\n✅ Pre-deployment checks complete. Run 'flyctl deploy' when ready.")
    
    print("\n📖 For more info: https://fly.io/docs/django/")

if __name__ == '__main__':
    main()