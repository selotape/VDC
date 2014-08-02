import Consts
from MachineDetails import MachineDetails
import boto.ec2
import time
import threading

class VDCConnection:

    def __init__(self, access_id=None, access_key=None, region=Consts.DEFAULT_REGION):
        """

        :param access_id: currently unused, assumes boto_config.ini file (@TODO)
        :param access_key: currently unused, assumes boto_config.ini file (@TODO)
        :param region: the region to use
        """
        self.access_id = access_id
        self.access_key = access_key
        self.conn = boto.ec2.connect_to_region(region)
        assert self.conn, "Connection could not be made!"

    @staticmethod
    def __stop_new_machine(instance):
        i = 0
        while instance.state == "pending":
            time.sleep(5)
            i += 5
            assert i < 150
        instance.stop()

    def create_machine(self, name, ami, key_name, instance_type=Consts.FREE_INSTANCE_TYPE, tags=None, allowed_ip_prefixes=Consts.EVERYONE):
        """
        Creates a new instances.
        :param name: name of the instance.
        :param ami: ami to clone.
        :param key_name: name of the key-pair to be used.
        :param instance_type: aws instance type.
        :param tags: tags to associate with the instance (currently unused. @TODO).
        :param allowed_ip_prefixes: IPs to be allowed MSTSC in the security group (currently unused. @TODO).
        :return: a MachineDetails object describing the newly created machine
        """
        res = self.conn.run_instances(ami, key_name=key_name, instance_type=instance_type, security_groups=["default"])
        inst = res.instances[0]
        assert inst, "Machine creation failed!"
        inst.add_tag("Name", name)
        #t = threading.Thread(target=self.__stop_new_machine, args=[inst])
        #t.start()
        return MachineDetails(inst)

    def get_all_instances(self, tags=None):
        """
        Returns all instances in the account.
        :param tags: currently unused.
        :return: a list of tuples (id, name).
        """
        instances = [i.instances[0] for i in self.conn.get_all_instances()]
        #return [(inst.id, inst.__dict__["tags"]["Name"]) for inst in instants]
        return [MachineDetails(inst) for inst in instances]

    def terminate_machine(self, instance_id):
        self.conn.terminate_instances([instance_id])

    def start_usage(self, instance_id):
        pass

    def stop_usage(self, instance_id):
        pass
