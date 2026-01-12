#!/usr/bin/env python3
"""
CommitCadence Automation Script (Python)
Cross-platform version that works on Windows, Mac, and Linux
"""

import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path

def run_command(cmd, cwd=None, shell=False):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=shell,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        print(f"Error message: {e.stderr}")
        return None

def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")
    
    # Check Java
    java_check = run_command(["java", "-version"], shell=False)
    if java_check is None:
        print("❌ Java is not installed. Please install Java Runtime Environment (JRE 8+)")
        print("   Download from: https://www.oracle.com/java/technologies/downloads/")
        return False
    print("✓ Java is installed")
    
    # Check Git
    git_check = run_command(["git", "--version"], shell=False)
    if git_check is None:
        print("❌ Git is not installed. Please install Git")
        print("   Download from: https://git-scm.com/downloads")
        return False
    print("✓ Git is installed")
    
    return True

def get_user_input():
    """Get user configuration"""
    print("\n" + "="*50)
    print("CommitCadence Setup")
    print("="*50 + "\n")
    
    print("Step 1: GitHub Configuration")
    email = input("Enter your GitHub email address: ").strip()
    if not email:
        print("Error: Email address is required!")
        sys.exit(1)
    
    print(f"Email configured: {email}")
    
    print("\nStep 2: Repository Setup")
    repo_name = input("Enter your GitHub repository name (e.g., commit-art): ").strip()
    if not repo_name:
        print("Error: Repository name is required!")
        sys.exit(1)
    
    repo_url = input("Enter your GitHub repository URL: ").strip()
    if not repo_url:
        print("Error: Repository URL is required!")
        sys.exit(1)
    
    # Validate URL format
    if not (repo_url.startswith("https://") or repo_url.startswith("git@")):
        print("Error: URL must start with 'https://' or 'git@'")
        sys.exit(1)
    
    return email, repo_name, repo_url

def launch_grid_editor():
    """Launch the Java grid editor"""
    script_dir = Path(__file__).parent
    jar_path = script_dir / "dist" / "Selectable_Grid.jar"
    
    if not jar_path.exists():
        print(f"❌ Error: Grid editor not found at {jar_path}")
        sys.exit(1)
    
    print("\nStep 4: Design Your Pattern")
    print("="*50)
    print("\nInstructions:")
    print("  - LEFT CLICK on cells to cycle through colors")
    print("  - RIGHT CLICK anywhere when done to save your design")
    print("  - Enter the date when you want the pattern to appear")
    print("  - Close the window after saving")
    print("")
    input("Press ENTER to launch the designer...")
    
    # Run Java GUI and wait for it to close
    try:
        subprocess.run(["java", "-jar", str(jar_path)], cwd=jar_path.parent, check=True)
    except subprocess.CalledProcessError:
        print("❌ Error launching grid editor")
        sys.exit(1)
    
    # Check if dates.txt was created
    dates_file = script_dir / "dist" / "dates.txt"
    if not dates_file.exists():
        print("❌ Error: dates.txt was not generated. Did you right-click to save your design?")
        sys.exit(1)
    
    print("\nDesign file found!")
    return dates_file

def create_commits(email, repo_name, repo_url, dates_file):
    """Create and push backdated commits"""
    script_dir = Path(__file__).parent
    paint_script = script_dir / "paint-interactive.sh"
    
    if not paint_script.exists():
        print(f"❌ Error: paint-interactive.sh not found")
        sys.exit(1)
    
    # Create temporary repository
    import time
    temp_dir = Path(f"/tmp/commitcadence-{repo_name}-{int(time.time())}")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nCreating temporary repository at: {temp_dir}")
    
    try:
        # Initialize git repo
        run_command(["git", "init"], cwd=str(temp_dir))
        
        # Create initial README
        readme_path = temp_dir / "README.md"
        readme_path.write_text(f"# {repo_name}\n")
        
        run_command(["git", "add", "README.md"], cwd=str(temp_dir))
        run_command(["git", "commit", "-m", "Initial commit"], cwd=str(temp_dir))
        run_command(["git", "remote", "add", "origin", repo_url], cwd=str(temp_dir))
        
        print("Repository initialized!")
        
        # Step 3: Configure git email
        print("\nStep 3: Configuring Git")
        run_command(["git", "config", "--local", "user.email", email], cwd=str(temp_dir))
        print(f"Git configured with email: {email}")
        
        # Copy necessary files
        print("\nStep 5: Applying Your Design")
        shutil.copy(dates_file, temp_dir)
        shutil.copy(paint_script, temp_dir)
        
        # Make paint script executable (Unix-like systems)
        if os.name != 'nt':  # Not Windows
            os.chmod(temp_dir / "paint-interactive.sh", 0o755)
        
        print("Applying commits to create your design...")
        print("")
        
        # Copy necessary files
        shutil.copy(dates_file, temp_dir)
        shutil.copy(paint_script, temp_dir)
        
        # Make paint script executable (Unix-like systems)
        if os.name != 'nt':  # Not Windows
            os.chmod(Path(temp_dir) / "paint-interactive.sh", 0o755)
        
        print("\n" + "="*50)
        print("Creating Commits...")
        print("="*50 + "\n")
        
        # Run paint script
        if os.name == 'nt':  # Windows
            # Try Git Bash if available
            git_bash = Path("C:/Program Files/Git/bin/bash.exe")
            if git_bash.exists():
                subprocess.run(
                    [str(git_bash), "paint-interactive.sh", "dates.txt"],
                    cwd=str(temp_dir),
                    check=True
                )
            else:
                print("❌ Git Bash not found. Please install Git for Windows.")
                print("   Download from: https://gitforwindows.org/")
                sys.exit(1)
        else:  # Unix-like (Mac, Linux)
            subprocess.run(
                ["bash", "paint-interactive.sh", "dates.txt"],
                cwd=str(temp_dir),
                check=True
            )
        
        print("\n" + "="*50)
        print("   Success! CommitCadence art is ready!")
        print("="*50)
        print("\n✨ Your art has been created!")
        print("\nNext steps:")
        print("1. Wait 5-10 minutes for GitHub to update")
        print("2. Visit your profile to see your contribution graph")
        print("3. Share your awesome creation!")
        print(f"\nRepository location: {temp_dir}")
        print("This temporary directory will be auto-cleaned from /tmp")
        
    except Exception as e:
        print(f"\n❌ Error during commit creation: {e}")
        sys.exit(1)

def main():
    """Main execution flow"""
    print("\n" + "="*50)
    print("   CommitCadence - Automated Setup")
    print("="*50)
    print("\nCreate beautiful GitHub contribution art!")
    print("")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Get user input
    email, repo_name, repo_url = get_user_input()
    
    # Launch grid editor
    dates_file = launch_grid_editor()
    
    # Create and push commits
    create_commits(email, repo_name, repo_url, dates_file)
    
    print("\nPress ENTER to exit...")
    input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
