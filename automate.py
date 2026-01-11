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
    
    email = input("Enter your GitHub email: ").strip()
    if not email:
        print("Error: Email is required")
        sys.exit(1)
    
    repo_url = input("Enter your repository URL (e.g., https://github.com/username/repo.git): ").strip()
    if not repo_url:
        print("Error: Repository URL is required")
        sys.exit(1)
    
    start_date = input("Enter start date (must be a Sunday, format: dd/MM/yyyy): ").strip()
    if not start_date:
        print("Error: Start date is required")
        sys.exit(1)
    
    return email, repo_url, start_date

def launch_grid_editor():
    """Launch the Java grid editor"""
    script_dir = Path(__file__).parent
    jar_path = script_dir / "dist" / "Selectable_Grid.jar"
    
    if not jar_path.exists():
        print(f"❌ Error: Grid editor not found at {jar_path}")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("Launching Grid Editor...")
    print("="*50)
    print("\nDesign your pattern:")
    print("- LEFT CLICK: Cycle through commit intensities")
    print("- RIGHT CLICK: Save design and enter date")
    print("\nWaiting for design completion...")
    
    # Run Java GUI and wait for it to close
    try:
        subprocess.run(["java", "-jar", str(jar_path)], check=True)
    except subprocess.CalledProcessError:
        print("❌ Error launching grid editor")
        sys.exit(1)
    
    # Check if dates.txt was created
    dates_file = script_dir / "dist" / "dates.txt"
    if not dates_file.exists():
        print("❌ Error: dates.txt not found. Make sure you right-clicked and saved your design.")
        sys.exit(1)
    
    print("✓ Design saved successfully!")
    return dates_file

def create_commits(email, repo_url, dates_file):
    """Create and push backdated commits"""
    script_dir = Path(__file__).parent
    paint_script = script_dir / "paint-interactive.sh"
    
    if not paint_script.exists():
        print(f"❌ Error: paint-interactive.sh not found")
        sys.exit(1)
    
    # Create temporary repository
    temp_dir = tempfile.mkdtemp(prefix="commitcadence_")
    print(f"\nCreating temporary repository at: {temp_dir}")
    
    try:
        # Initialize git repo
        run_command(["git", "init"], cwd=temp_dir)
        run_command(["git", "config", "user.email", email], cwd=temp_dir)
        run_command(["git", "config", "user.name", email.split("@")[0]], cwd=temp_dir)
        
        # Add remote
        run_command(["git", "remote", "add", "origin", repo_url], cwd=temp_dir)
        
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
                    cwd=temp_dir,
                    check=True
                )
            else:
                print("❌ Git Bash not found. Please install Git for Windows.")
                print("   Download from: https://gitforwindows.org/")
                sys.exit(1)
        else:  # Unix-like (Mac, Linux)
            subprocess.run(
                ["bash", "paint-interactive.sh", "dates.txt"],
                cwd=temp_dir,
                check=True
            )
        
        print("\n✓ All commits created and pushed successfully!")
        print(f"\nCheck your GitHub profile in 5-10 minutes to see the pattern.")
        
    except Exception as e:
        print(f"\n❌ Error during commit creation: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        try:
            shutil.rmtree(temp_dir)
            print(f"\n✓ Cleaned up temporary directory")
        except:
            pass

def main():
    """Main execution flow"""
    print("\n" + "="*50)
    print("CommitCadence - GitHub Contribution Art Tool")
    print("="*50 + "\n")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Get user input
    email, repo_url, start_date = get_user_input()
    
    # Launch grid editor
    dates_file = launch_grid_editor()
    
    # Create and push commits
    create_commits(email, repo_url, dates_file)
    
    print("\n" + "="*50)
    print("Done!")
    print("="*50)
    print("\nYour GitHub contribution pattern has been applied.")
    print("Visit your profile to see the design (may take 5-10 minutes to appear)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
