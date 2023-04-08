class Role:
    """
    Constants for the various roles scoped in the application ecosystem
    """

    GUEST = {
        "name": "GUEST",
        "description": "A Guest Account",
    }
    ACCOUNT_MEMEBER = {
        "name": "ACCOUNT_MEMEBER",
        "description": "Member of a maintenance team",
    }
    ACCOUNT_ADMIN = {
        "name": "ACCOUNT_ADMIN",
        "description": "Manager of a local entity",
    }
    FLEET_MANAGER = {
        "name": "FLEET_MANAGER",
        "description": "Manager of the fleet",
    }
    ADMIN = {
        "name": "ADMIN",
        "description": "Admin of Application Ecosystem",
    }
    SUPER_ADMIN = {
        "name": "SUPER_ADMIN",
        "description": "Super Administrator of Application Ecosystem",
    }
