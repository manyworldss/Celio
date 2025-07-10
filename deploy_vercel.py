#!/usr/bin/env python3
"""
Vercel Deployment Helper Script for Celio

This script helps prepare and deploy the Celio application to Vercel.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if all required files exist."""
    required_files = [
        'vercel.json',
        'build_files.sh',
        'requirements.txt',
        '.vercelignore',
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

def check_environment_variables():
    """Check if environment variables are set."""
    required_vars = [
        'DJANGO_SECRET_KEY',
        'DATABASE_URL',
        'VERCEL_BLOB_TOKEN'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Missing environment variables (set these in Vercel dashboard):")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print("✅ Environment variables configured")
    return True

def collect_static():
    """Collect static files."""
    print("📦 Collecting static files...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("✅ Static files collected")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error collecting static files: {e}")
        return False

def run_tests():
    """Run basic tests."""
    print("🧪 Running tests...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'check'], check=True)
        print("✅ Django checks passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Django checks failed: {e}")
        return False

def deploy_to_vercel():
    """Deploy to Vercel."""
    print("🚀 Deploying to Vercel...")
    try:
        subprocess.run(['vercel', '--prod'], check=True)
        print("✅ Deployment successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Vercel CLI not found. Install with: npm i -g vercel")
        return False

def main():
    """Main deployment process."""
    print("🔧 Celio Vercel Deployment Helper")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Please fix missing files before deploying.")
        return
    
    # Check environment (optional for local check)
    check_environment_variables()
    
    # Collect static files
    if not collect_static():
        print("\n❌ Static file collection failed.")
        return
    
    # Run tests
    if not run_tests():
        print("\n❌ Tests failed.")
        return
    
    # Ask for deployment confirmation
    deploy = input("\n🚀 Ready to deploy to Vercel? (y/N): ").lower().strip()
    if deploy == 'y':
        deploy_to_vercel()
    else:
        print("\n✅ Pre-deployment checks complete. Run 'vercel --prod' when ready.")
    
    print("\n📖 For detailed instructions, see VERCEL_DEPLOYMENT.md")

if __name__ == '__main__':
    main()