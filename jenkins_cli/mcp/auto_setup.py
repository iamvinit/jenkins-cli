import os
import yaml
from jenkins_cli.config import CONFIG_FILE, CONFIG_DIR, ensure_config_exists
from jenkins_cli.commands.init_cmd import init
from jenkins_cli.config.constants import LOCAL_CONFIG

async def auto_configure_jenkins():
    """Auto-configure Jenkins connection during MCP server startup"""
    # Check if config already exists
    if os.path.exists(CONFIG_FILE):
        return
    
    # Try to configure from environment variables
    jenkins_host = os.getenv('JENKINS_HOST')
    jenkins_user = os.getenv('JENKINS_USER') or os.getenv('JENKINS_USERNAME')
    jenkins_token = os.getenv('JENKINS_TOKEN') or os.getenv('JENKINS_API_TOKEN')
    
    if all([jenkins_host, jenkins_user, jenkins_token]):
        # Create config directory if it doesn't exist
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        # Create configuration
        config = {
            'host': jenkins_host,
            'user': jenkins_user,
            'token': jenkins_token
        }
        
        # Save configuration
        with open(CONFIG_FILE, 'w') as f:
            yaml.safe_dump(config, f)
        
        print(f"Jenkins configuration auto-configured from environment variables")
        print(f"Jenkins Host: {jenkins_host}")
        print(f"Jenkins User: {jenkins_user}")
    else:
        # Fall back to interactive configuration
        ensure_config_exists()

async def auto_initialize_job():
    """Auto-initialize job if in project directory"""
    if not os.path.exists(LOCAL_CONFIG):
        # Use default job name (current directory)
        init.callback(name=None, debug=False)
