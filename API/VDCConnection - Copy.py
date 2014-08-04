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

    def __stop_new_machine(self, instance):
        i = 0
        while instance.state == "pending":
            assert i < 150
            i += 5
            time.sleep(5)
            instance = self.conn.get_all_instances([instance.id])[0].instances[0]
        instance.stop()

    def create_machine(self, name, ami, key_name, instance_type=Consts.FREE_INSTANCE_TYPE, tags=None, allowed_ip_prefixes=Consts.EVERYONE):
        """
        Creates a new machine in stopped state.
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
        t = threading.Thread(target=self.__stop_new_machine, args=[inst])
        t.start()
        return MachineDetails(inst)

    def get_all_machines(self, tags=None):
        """
        Returns all machines in the account that contain the given tags.
        :param tags: tags that control which machines are returned (None means all machines in the account).
        :return: a list MachineDetails objects corresponding to the retrieved instances.
        """
        if tags:
            keys, values = tags.keys(), tags.values()
            filter_keys = map(lambda key: "tag:" + key, keys)
            filter_tags = dict(zip(filter_keys, values))
            res = self.conn.get_all_instances(filters=filter_tags)
        else:
            res = self.conn.get_all_instances()
        instances = [i.instances[0] for i in res]
        return [MachineDetails(inst) for inst in instances]

    def terminate_machine(self, instance_id):
        self.conn.terminate_instances([instance_id])

    def start_usage(self, instance_id):
        pass

    def stop_usage(self, instance_id):
        pass


