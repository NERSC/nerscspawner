
from sshspawner.sshspawner import SSHSpawner

c.NERSCSpawner.profiles = [
    { "name": "cori-shared-node-cpu" },
    { "name": "spin-shared-node-cpu" },
]

c.NERSCSpawner.setups = [
    { 
        "name": "shared-node",
        "architectures": [
            {
                "name": "cpu",
                "description": "Shared CPU Node",
            }
        ],
        "resources": "Use a node shared with other users' notebooks but outside the batch queues.",
        "use_cases": "Visualization and analytics that are not memory intensive and can run on just a few cores." 
    }
]

c.NERSCSpawner.systems = [
    { "name": "cori" },
    { "name": "spin" }
]

c.NERSCSpawner.spawners = {
    { 
        "cori-shared-node-cpu" : ( SSHSpawner, {} ),
        "spin-shared-node-cpu" : ( SSHSpawner, {} ),
    }
}
