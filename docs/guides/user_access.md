# User Access and Settings Guide

This guide covers user access management, permissions, settings configuration, and multi-user scenarios for perplSDK.

## Overview

This guide helps you:
- Set up user access and authentication
- Configure user permissions and roles
- Manage team access to perplSDK
- Configure user-specific settings
- Implement multi-user workflows

## User Setup

### Single User Setup

For individual use:

```python
from perplSDK.core.config import Config

# Create user-specific configuration
config = Config.from_env()

# Optionally save user preferences
config.save_to_file("~/.perplsdk/config.yaml")
```

### Environment Setup

Set up user-specific environment:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PERPLEXITY_API_KEY="your-personal-api-key"
export PERPLSDK_USER="john.doe@company.com"
export PERPLSDK_OUTPUT_DIR="$HOME/research/reports"
```

### User Preferences

Create user preference file:

```yaml
# ~/.perplsdk/preferences.yaml
user:
  name: John Doe
  email: john.doe@company.com
  department: Research

preferences:
  default_model: llama-3.1-sonar-large-128k-online
  default_output_dir: ~/research/reports
  auto_publish: false
  notification_email: john.doe@company.com

templates:
  default: comprehensive
  favorites:
    - ev_market_analysis
    - battery_tech_trends
```

## User Roles and Permissions

### Role Definitions

```python
from enum import Enum

class UserRole(Enum):
    """User role definitions."""
    ADMIN = "admin"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    VIEWER = "viewer"

class Permissions:
    """Permission definitions for each role."""
    
    ROLE_PERMISSIONS = {
        UserRole.ADMIN: [
            'read', 'write', 'delete',
            'publish', 'configure',
            'manage_users', 'access_all_projects'
        ],
        UserRole.RESEARCHER: [
            'read', 'write',
            'publish_own', 'configure_own'
        ],
        UserRole.ANALYST: [
            'read', 'write',
            'view_reports'
        ],
        UserRole.VIEWER: [
            'read', 'view_reports'
        ]
    }
    
    @classmethod
    def get_permissions(cls, role: UserRole):
        """Get permissions for a role."""
        return cls.ROLE_PERMISSIONS.get(role, [])
```

### User Access Control

```python
class User:
    """User with role-based access control."""
    
    def __init__(self, username, email, role: UserRole):
        self.username = username
        self.email = email
        self.role = role
        self.permissions = Permissions.get_permissions(role)
    
    def can(self, permission):
        """Check if user has permission."""
        return permission in self.permissions
    
    def can_access_project(self, project):
        """Check if user can access a project."""
        if 'access_all_projects' in self.permissions:
            return True
        return project.owner == self.username
    
    def can_publish(self):
        """Check if user can publish reports."""
        return 'publish' in self.permissions or 'publish_own' in self.permissions

# Create users
admin = User("admin@company.com", "Admin User", UserRole.ADMIN)
researcher = User("researcher@company.com", "Jane Researcher", UserRole.RESEARCHER)
viewer = User("viewer@company.com", "View Only", UserRole.VIEWER)

# Check permissions
if researcher.can('write'):
    # Conduct research
    pass

if admin.can('manage_users'):
    # Manage user accounts
    pass
```

### Access Control Implementation

```python
class AccessControlledResearch:
    """Research automation with access control."""
    
    def __init__(self, user: User, config: Config):
        self.user = user
        self.config = config
        self.research = ResearchAutomation(config)
    
    def create_project(self, name, description):
        """Create project with ownership."""
        if not self.user.can('write'):
            raise PermissionError(f"User {self.user.username} cannot create projects")
        
        project = self.research.create_project(name, description)
        project.owner = self.user.username
        project.metadata['created_by'] = self.user.username
        project.metadata['created_at'] = datetime.now().isoformat()
        
        return project
    
    def access_project(self, project_name):
        """Access project with permission check."""
        project = self.research.get_project(project_name)
        
        if not project:
            raise ValueError(f"Project {project_name} not found")
        
        if not self.user.can_access_project(project):
            raise PermissionError(f"User {self.user.username} cannot access this project")
        
        return project
    
    def publish_report(self, project_name):
        """Publish report with permission check."""
        if not self.user.can_publish():
            raise PermissionError(f"User {self.user.username} cannot publish reports")
        
        project = self.access_project(project_name)
        
        # Publish logic
        github = GitHubPublisher(self.config)
        # ... publish report

# Use access-controlled research
user = User("john@company.com", "John Doe", UserRole.RESEARCHER)
research = AccessControlledResearch(user, config)

project = research.create_project("My Research", "Description")
```

## Team Access Management

### Team Configuration

```python
class Team:
    """Team with shared access."""
    
    def __init__(self, name):
        self.name = name
        self.members = {}
        self.shared_projects = []
    
    def add_member(self, user: User):
        """Add team member."""
        self.members[user.username] = user
    
    def remove_member(self, username):
        """Remove team member."""
        if username in self.members:
            del self.members[username]
    
    def add_shared_project(self, project_name):
        """Add project to team's shared projects."""
        self.shared_projects.append(project_name)
    
    def can_access_project(self, username, project_name):
        """Check if team member can access project."""
        if username not in self.members:
            return False
        
        user = self.members[username]
        
        # Check if project is shared with team
        if project_name in self.shared_projects:
            return user.can('read')
        
        return False

# Create team
ev_research_team = Team("EV Research Team")
ev_research_team.add_member(User("alice@company.com", "Alice", UserRole.RESEARCHER))
ev_research_team.add_member(User("bob@company.com", "Bob", UserRole.ANALYST))

# Share project with team
ev_research_team.add_shared_project("EV Market Analysis")

# Check access
can_access = ev_research_team.can_access_project("alice@company.com", "EV Market Analysis")
```

### Shared Resources

```python
class SharedResourceManager:
    """Manage shared research resources."""
    
    def __init__(self):
        self.shared_templates = {}
        self.shared_configs = {}
        self.shared_reports = {}
    
    def share_template(self, template_name, template, teams):
        """Share template with teams."""
        self.shared_templates[template_name] = {
            'template': template,
            'teams': teams,
            'shared_by': current_user,
            'shared_at': datetime.now()
        }
    
    def get_shared_templates(self, user: User):
        """Get templates shared with user."""
        user_teams = get_user_teams(user.username)
        
        shared = []
        for name, data in self.shared_templates.items():
            if any(team in data['teams'] for team in user_teams):
                shared.append((name, data['template']))
        
        return shared
    
    def share_config(self, config_name, config, teams):
        """Share configuration with teams."""
        self.shared_configs[config_name] = {
            'config': config,
            'teams': teams
        }

# Use shared resources
resource_mgr = SharedResourceManager()

# Share template
template = ResearchTemplate()
resource_mgr.share_template(
    "EV Analysis Template",
    template,
    teams=["EV Research Team", "Market Intelligence Team"]
)

# Get shared templates for user
user_templates = resource_mgr.get_shared_templates(current_user)
```

## User Settings

### Personal Settings

```python
class UserSettings:
    """User-specific settings."""
    
    def __init__(self, username):
        self.username = username
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load user settings."""
        settings_file = f"~/.perplsdk/settings_{self.username}.yaml"
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                return yaml.safe_load(f)
        return self.get_default_settings()
    
    def get_default_settings(self):
        """Get default settings."""
        return {
            'research': {
                'default_model': 'llama-3.1-sonar-small-128k-online',
                'default_temperature': 0.2,
                'parallel_execution': True,
                'max_parallel_queries': 5
            },
            'reports': {
                'default_format': 'markdown',
                'include_sources': True,
                'include_citations': True,
                'auto_publish': False
            },
            'notifications': {
                'email_enabled': True,
                'email_address': f"{self.username}@company.com",
                'slack_enabled': False,
                'notify_on_completion': True,
                'notify_on_error': True
            },
            'ui': {
                'theme': 'light',
                'items_per_page': 20,
                'show_progress': True
            }
        }
    
    def save_settings(self):
        """Save user settings."""
        settings_file = f"~/.perplsdk/settings_{self.username}.yaml"
        os.makedirs(os.path.dirname(settings_file), exist_ok=True)
        
        with open(settings_file, 'w') as f:
            yaml.dump(self.settings, f)
    
    def get(self, key, default=None):
        """Get setting value."""
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """Set setting value."""
        keys = key.split('.')
        setting = self.settings
        
        for k in keys[:-1]:
            if k not in setting:
                setting[k] = {}
            setting = setting[k]
        
        setting[keys[-1]] = value
        self.save_settings()

# Use user settings
settings = UserSettings("john.doe")

# Get settings
default_model = settings.get('research.default_model')
auto_publish = settings.get('reports.auto_publish')

# Update settings
settings.set('research.parallel_execution', False)
settings.set('notifications.email_enabled', True)
```

### Configuration Profiles

```python
class ConfigurationProfile:
    """User configuration profile."""
    
    def __init__(self, username):
        self.username = username
        self.profiles = {}
        self.active_profile = "default"
    
    def create_profile(self, name, config):
        """Create configuration profile."""
        self.profiles[name] = config
    
    def switch_profile(self, name):
        """Switch to different profile."""
        if name in self.profiles:
            self.active_profile = name
        else:
            raise ValueError(f"Profile {name} not found")
    
    def get_active_config(self):
        """Get active configuration."""
        return self.profiles.get(self.active_profile)

# Use profiles
profiles = ConfigurationProfile("john.doe")

# Create profiles for different scenarios
profiles.create_profile("development", Config(
    perplexity_api_key="dev-key",
    api_rate_limit=30,
    log_level="DEBUG"
))

profiles.create_profile("production", Config(
    perplexity_api_key="prod-key",
    api_rate_limit=60,
    log_level="WARNING"
))

# Switch profiles
profiles.switch_profile("development")
config = profiles.get_active_config()
```

## Multi-User Workflows

### Collaborative Research

```python
class CollaborativeProject:
    """Project with multiple collaborators."""
    
    def __init__(self, name, owner: User):
        self.name = name
        self.owner = owner
        self.collaborators = [owner]
        self.permissions = {owner.username: ['read', 'write', 'admin']}
    
    def add_collaborator(self, user: User, permissions):
        """Add collaborator with specific permissions."""
        self.collaborators.append(user)
        self.permissions[user.username] = permissions
    
    def remove_collaborator(self, username):
        """Remove collaborator."""
        self.collaborators = [c for c in self.collaborators if c.username != username]
        if username in self.permissions:
            del self.permissions[username]
    
    def can_user_modify(self, username):
        """Check if user can modify project."""
        return 'write' in self.permissions.get(username, [])
    
    def can_user_admin(self, username):
        """Check if user can administer project."""
        return 'admin' in self.permissions.get(username, [])

# Create collaborative project
owner = User("alice@company.com", "Alice", UserRole.RESEARCHER)
project = CollaborativeProject("Shared EV Analysis", owner)

# Add collaborators
bob = User("bob@company.com", "Bob", UserRole.ANALYST)
project.add_collaborator(bob, ['read', 'write'])

charlie = User("charlie@company.com", "Charlie", UserRole.VIEWER)
project.add_collaborator(charlie, ['read'])
```

### Review Workflow

```python
class ReviewWorkflow:
    """Workflow for report review and approval."""
    
    def __init__(self, report, author: User):
        self.report = report
        self.author = author
        self.reviewers = []
        self.reviews = {}
        self.status = "draft"
    
    def add_reviewer(self, reviewer: User):
        """Add reviewer."""
        self.reviewers.append(reviewer)
    
    def submit_review(self, reviewer: User, approved, comments):
        """Submit review."""
        if reviewer not in self.reviewers:
            raise PermissionError("User is not a reviewer")
        
        self.reviews[reviewer.username] = {
            'approved': approved,
            'comments': comments,
            'timestamp': datetime.now()
        }
        
        self.update_status()
    
    def update_status(self):
        """Update workflow status based on reviews."""
        if len(self.reviews) == 0:
            self.status = "pending_review"
        elif all(r['approved'] for r in self.reviews.values()):
            self.status = "approved"
        elif any(not r['approved'] for r in self.reviews.values()):
            self.status = "needs_revision"
    
    def can_publish(self):
        """Check if report can be published."""
        return self.status == "approved"

# Use review workflow
report = "Q4 EV Market Analysis"
workflow = ReviewWorkflow(report, researcher)

# Add reviewers
workflow.add_reviewer(senior_researcher)
workflow.add_reviewer(team_lead)

# Submit reviews
workflow.submit_review(senior_researcher, True, "Looks good!")
workflow.submit_review(team_lead, True, "Approved")

# Check if can publish
if workflow.can_publish():
    publish_report(report)
```

## User Activity Tracking

### Activity Logging

```python
class UserActivityTracker:
    """Track user activity."""
    
    def __init__(self):
        self.activities = []
    
    def log_activity(self, user: User, action, details):
        """Log user activity."""
        activity = {
            'timestamp': datetime.now().isoformat(),
            'user': user.username,
            'email': user.email,
            'role': user.role.value,
            'action': action,
            'details': details
        }
        
        self.activities.append(activity)
        self.save_to_log(activity)
    
    def save_to_log(self, activity):
        """Save activity to log file."""
        with open('user_activity.log', 'a') as f:
            f.write(json.dumps(activity) + '\n')
    
    def get_user_activities(self, username, start_date=None, end_date=None):
        """Get activities for a user."""
        user_activities = [a for a in self.activities if a['user'] == username]
        
        if start_date:
            user_activities = [a for a in user_activities 
                             if datetime.fromisoformat(a['timestamp']) >= start_date]
        
        if end_date:
            user_activities = [a for a in user_activities 
                             if datetime.fromisoformat(a['timestamp']) <= end_date]
        
        return user_activities

# Use activity tracker
tracker = UserActivityTracker()

# Log activities
tracker.log_activity(user, "create_project", {"project": "EV Analysis"})
tracker.log_activity(user, "conduct_research", {"project": "EV Analysis", "queries": 5})
tracker.log_activity(user, "publish_report", {"report": "ev_analysis.md"})

# Get user activities
activities = tracker.get_user_activities("john.doe@company.com")
```

### Usage Analytics

```python
class UsageAnalytics:
    """Analyze user usage patterns."""
    
    def __init__(self, tracker: UserActivityTracker):
        self.tracker = tracker
    
    def get_user_stats(self, username):
        """Get usage statistics for user."""
        activities = self.tracker.get_user_activities(username)
        
        return {
            'total_activities': len(activities),
            'projects_created': len([a for a in activities if a['action'] == 'create_project']),
            'researches_conducted': len([a for a in activities if a['action'] == 'conduct_research']),
            'reports_published': len([a for a in activities if a['action'] == 'publish_report']),
            'last_activity': activities[-1]['timestamp'] if activities else None
        }
    
    def get_team_stats(self, team: Team):
        """Get usage statistics for team."""
        team_stats = {}
        
        for username in team.members:
            team_stats[username] = self.get_user_stats(username)
        
        return team_stats

# Use analytics
analytics = UsageAnalytics(tracker)
user_stats = analytics.get_user_stats("john.doe@company.com")
team_stats = analytics.get_team_stats(ev_research_team)
```

## Best Practices

### 1. Principle of Least Privilege

Grant users minimum necessary permissions:

```python
# Good - minimal permissions
viewer = User("viewer@company.com", "Viewer", UserRole.VIEWER)

# Bad - excessive permissions
# Don't make everyone an admin
```

### 2. Regular Access Reviews

```python
def review_user_access():
    """Review and audit user access."""
    users = get_all_users()
    
    for user in users:
        # Check last activity
        last_activity = get_last_activity(user)
        
        # Deactivate inactive users
        if inactive_for_90_days(last_activity):
            deactivate_user(user)
        
        # Review permissions
        if needs_permission_review(user):
            notify_admin_for_review(user)
```

### 3. Clear Ownership

```python
# Always set project owner
project.owner = user.username
project.metadata['created_by'] = user.username

# Track modifications
project.metadata['last_modified_by'] = user.username
project.metadata['last_modified_at'] = datetime.now().isoformat()
```

### 4. Audit Trails

Maintain comprehensive audit trails:

```python
# Log all significant actions
tracker.log_activity(user, "delete_project", {"project": project_name})
tracker.log_activity(user, "change_permissions", {"target_user": target, "new_role": new_role})
```

## See Also

- [Privacy and Security Guide](privacy_and_security.md)
- [Configuration Guide](configuration.md)
- [Automated Workflows](automation.md)
