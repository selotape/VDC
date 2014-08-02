__author__ = 'Liahav Eitan'

import boto.ec2
import boto.ec2.elb
import os
import sys

# Region-specific constants
DEFAULT_REGION = "us-east-1"
DEFAULT_AMI = "ami-cfc9c0a6"  # Windows 2012
DEFAULT_KEY_NAME = "key1"

# Global constants
DEFAULT_INSTANCE_TYPE = "t1.micro"
DEFAULT_SECURITY_GROUP = "default"
DEFAULT_BALANCER_PORTS = [(80, 80, "http")]

### Commented out because changing regions requires changing AMI, key-pair ###
'''
def get_region():
    print "Choose a region of the following: (recommended: 'us-east-1')"
    regions = [reg.name for reg in boto.ec2.get_regions("ec2")]
    for reg in regions:
        print "\t%s" % reg
    region_name = raw_input()
    assert region_name in regions, "No such region %s" % region_name
    return boto.ec2.get_region(region_name)
'''

def get_availability_zones(conn):
    """
    Prints to the user all of the availability zones in the region of the current connection,
    and asks the user to choose two of the zones.
    :param conn An active connection to an EC2 region
    :return The names of the two chosen zones (asserted valid and not the same zone).
    """
    all_zones = [zone.name for zone in conn.get_all_zones()]
    print "Enter availability zones of the following:"
    for zone in all_zones:
        print "\t%s" % zone
    zone_1 = raw_input("1st zone: ")
    assert zone_1 in all_zones, "No such zone %s" % zone_1
    zone_2 = raw_input("2nd zone: ")
    assert zone_2 in all_zones, "No such zone %s" % zone_2
    assert zone_1 != zone_2, "You must choose two different zones!"
    return zone_1, zone_2

def create_instance(conn, zone):
    """
    Creates and runs a new instance of default AMI with default key-pair and security group.
    :param conn An active connection to an EC2 region on which the instance will be run.
    :param zone The availability zone where the instance will be placed.
    :return The ID of the new instance.
    """
    res = conn.run_instances(DEFAULT_AMI, key_name=DEFAULT_KEY_NAME, instance_type=DEFAULT_INSTANCE_TYPE,
                             security_groups=[DEFAULT_SECURITY_GROUP], placement=zone)
    inst = res.instances[0]
    print "Created instance %s" % inst.id
    return inst

def create_load_balancer(region, zones):
    """
    Creates a new load balancer that forwards the default ports.
    This function does NOT register instances to the load balancer.
    :param region The name of the region to create the load balancer in.
    :param zones List of availability zone names in the region where the load balancer should be available.
    :return The new LoadBalancer object.
    """
    conn = boto.ec2.elb.connect_to_region(region)
    name = raw_input("Enter a name for the load balancer: ")
    print "Creating load balancer..."
    lb = conn.create_load_balancer(name, zones, DEFAULT_BALANCER_PORTS)
    print "Created %s" % str(lb)
    return lb

def launch():
    """
    The main function for creating the entire structure. It:
    1) Prompts the user to choose two availability zones in the default region.
    2) Creates two instances, one on each zone.
    3) Creates a load balancer that is available on both zones.
    4) Registers both instances to the load balancer.
    """
    conn = boto.ec2.connect_to_region(DEFAULT_REGION)
    zones = get_availability_zones(conn)
    print "Creating instances..."
    inst1 = create_instance(conn, zones[0])
    inst2 = create_instance(conn, zones[1])
    lb = create_load_balancer(DEFAULT_REGION, zones)
    print "Registering instances to the load balancer..."
    lb.register_instances([inst1.id, inst2.id])
    print "Done!"

def terminate():
    """
    The main function for tearing down the entire structure.
    It prompts the user for confirmation before proceeding.
    BEWARE: It removes ALL instances and ALL load balancers in the default region.
    """
    conn = boto.ec2.connect_to_region(DEFAULT_REGION)
    elb_conn = boto.ec2.elb.connect_to_region(DEFAULT_REGION)
    instances = [r.instances[0].id for r in conn.get_all_instances()]
    load_balancers = [lb.name for lb in elb_conn.get_all_load_balancers()]
    prompt = "This will terminate %d instances and %d load balancers. " \
             "Are you sure? (yes/no)\n" % (len(instances), len(load_balancers))
    answer = raw_input(prompt)
    if answer == "yes":
        print "Terminating all instances"
        conn.terminate_instances(instances)
        print "Terminating all load balancers"
        for lb in load_balancers:
            elb_conn.delete_load_balancer(lb)
        print "Done!"
    else:
        print "Aborted!"

def usage():
    print "Usage:"
    print "\t%s [/terminate]" % os.path.basename(sys.argv[0])

def main():
    """
    Checks parameters and decides whether to launch instances, terminate instances or pring usage.
    """
    if len(sys.argv) == 1:
        launch()
        #create_load_balancer(boto.ec2.get_region("eu-west-1"), ["eu-west-1a", "eu-west-1b"])
    elif len(sys.argv) == 2 and sys.argv[1] == "/terminate":
        terminate()
    else:
        usage()

if __name__ == '__main__':
    main()
