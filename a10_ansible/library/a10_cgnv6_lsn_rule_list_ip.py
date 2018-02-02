#!/usr/bin/python

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = """
module: a10_cgnv6_lsn_rule_list_ip
description:
    - None
short_description: Configures A10 cgnv6.lsn.rule.list.ip
author: A10 Networks 2018 
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
        - present
        - absent
        required: True
    a10_host:
        description:
        - Host for AXAPI authentication
        required: True
    a10_username:
        description:
        - Username for AXAPI authentication
        required: True
    a10_password:
        description:
        - Password for AXAPI authentication
        required: True
    ipv4_addr:
        description:
        - "None"
        required: True
    rule_cfg:
        description:
        - "Field rule_cfg"
        required: False
        suboptions:
            proto:
                description:
                - "None"
            tcp_cfg:
                description:
                - "Field tcp_cfg"
            udp_cfg:
                description:
                - "Field udp_cfg"
            icmp_others_cfg:
                description:
                - "Field icmp_others_cfg"
            dscp_cfg:
                description:
                - "Field dscp_cfg"
    uuid:
        description:
        - "None"
        required: False
    user_tag:
        description:
        - "None"
        required: False
    sampling_enable:
        description:
        - "Field sampling_enable"
        required: False
        suboptions:
            counters1:
                description:
                - "None"


"""

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["ipv4_addr","rule_cfg","sampling_enable","user_tag","uuid",]

# our imports go at the top so we fail fast.
try:
    from a10_ansible import errors as a10_ex
    from a10_ansible.axapi_http import client_factory
    from a10_ansible.kwbl import KW_IN, KW_OUT, translate_blacklist as translateBlacklist

except (ImportError) as ex:
    module.fail_json(msg="Import Error:{0}".format(ex))
except (Exception) as ex:
    module.fail_json(msg="General Exception in Ansible module import:{0}".format(ex))


def get_default_argspec():
    return dict(
        a10_host=dict(type='str', required=True),
        a10_username=dict(type='str', required=True),
        a10_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="present", choices=["present", "absent"])
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        ipv4_addr=dict(type='str',required=True,),
        rule_cfg=dict(type='list',proto=dict(type='str',choices=['tcp','udp','icmp','others','dscp']),tcp_cfg=dict(type='dict',start_port=dict(type='int',),end_port=dict(type='int',),action_cfg=dict(type='str',choices=['action','no-action']),action_type=dict(type='str',choices=['dnat','drop','one-to-one-snat','pass-through','snat','set-dscp','template','idle-timeout']),ipv4_list=dict(type='str',),port_list=dict(type='str',),no_snat=dict(type='bool',),vrid=dict(type='int',),pool=dict(type='str',),shared=dict(type='bool',),http_alg=dict(type='str',),timeout_val=dict(type='int',),fast=dict(type='str',choices=['fast']),dscp_direction=dict(type='str',choices=['inbound','outbound']),dscp_value=dict(type='str',choices=['default','af11','af12','af13','af21','af22','af23','af31','af32','af33','af41','af42','af43','cs1','cs2','cs3','cs4','cs5','cs6','cs7','ef','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63'])),udp_cfg=dict(type='dict',start_port=dict(type='int',),end_port=dict(type='int',),action_cfg=dict(type='str',choices=['action','no-action']),action_type=dict(type='str',choices=['dnat','drop','one-to-one-snat','pass-through','snat','set-dscp','idle-timeout']),ipv4_list=dict(type='str',),port_list=dict(type='str',),no_snat=dict(type='bool',),vrid=dict(type='int',),pool=dict(type='str',),shared=dict(type='bool',),timeout_val=dict(type='int',),fast=dict(type='str',choices=['fast']),dscp_direction=dict(type='str',choices=['inbound','outbound']),dscp_value=dict(type='str',choices=['default','af11','af12','af13','af21','af22','af23','af31','af32','af33','af41','af42','af43','cs1','cs2','cs3','cs4','cs5','cs6','cs7','ef','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63'])),icmp_others_cfg=dict(type='dict',action_cfg=dict(type='str',choices=['action','no-action']),action_type=dict(type='str',choices=['dnat','drop','one-to-one-snat','pass-through','snat','set-dscp']),ipv4_list=dict(type='str',),no_snat=dict(type='bool',),vrid=dict(type='int',),pool=dict(type='str',),shared=dict(type='bool',),dscp_direction=dict(type='str',choices=['inbound','outbound']),dscp_value=dict(type='str',choices=['default','af11','af12','af13','af21','af22','af23','af31','af32','af33','af41','af42','af43','cs1','cs2','cs3','cs4','cs5','cs6','cs7','ef','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63'])),dscp_cfg=dict(type='dict',dscp_match=dict(type='str',choices=['default','af11','af12','af13','af21','af22','af23','af31','af32','af33','af41','af42','af43','cs1','cs2','cs3','cs4','cs5','cs6','cs7','ef','any','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63']),action_cfg=dict(type='str',choices=['action']),action_type=dict(type='str',choices=['set-dscp']),dscp_direction=dict(type='str',choices=['inbound','outbound']),dscp_value=dict(type='str',choices=['default','af11','af12','af13','af21','af22','af23','af31','af32','af33','af41','af42','af43','cs1','cs2','cs3','cs4','cs5','cs6','cs7','ef','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63']))),
        uuid=dict(type='str',),
        user_tag=dict(type='str',),
        sampling_enable=dict(type='list',counters1=dict(type='str',choices=['all','placeholder']))
    ))

    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/cgnv6/lsn-rule-list/{name}/ip/{ipv4-addr}"
    f_dict = {}
    f_dict["ipv4-addr"] = ""

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/cgnv6/lsn-rule-list/{name}/ip/{ipv4-addr}"
    f_dict = {}
    f_dict["ipv4-addr"] = module.params["ipv4-addr"]

    return url_base.format(**f_dict)


def build_envelope(title, data):
    return {
        title: data
    }

def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")

def _build_dict_from_param(param):
    rv = {}

    for k,v in param.items():
        hk = _to_axapi(k)
        if isinstance(v, dict):
            v_dict = _build_dict_from_param(v)
            rv[hk] = v_dict
        if isinstance(v, list):
            nv = [_build_dict_from_param(x) for x in v]
            rv[hk] = nv
        else:
            rv[hk] = v

    return rv

def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v:
            rx = _to_axapi(x)

            if isinstance(v, dict):
                nv = _build_dict_from_param(v)
                rv[rx] = nv
            if isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)

def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([x for x in requires_one_of if params.get(x)])
    
    errors = []
    marg = []
    
    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc,msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc,msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc,msg = REQUIRED_VALID
    
    if not rc:
        errors.append(msg.format(", ".join(marg)))
    
    return rc,errors

def exists(module):
    try:
        module.client.get(existing_url(module))
        return True
    except a10_ex.NotFound:
        return False

def create(module, result):
    payload = build_json("ip", module)
    try:
        post_result = module.client.post(new_url(module), payload)
        result.update(**post_result)
        result["changed"] = True
    except a10_ex.Exists:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def delete(module, result):
    try:
        module.client.delete(existing_url(module))
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def update(module, result):
    payload = build_json("ip", module)
    try:
        post_result = module.client.put(existing_url(module), payload)
        result.update(**post_result)
        result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def present(module, result):
    if not exists(module):
        return create(module, result)
    else:
        return update(module, result)

def absent(module, result):
    return delete(module, result)

def run_command(module):
    run_errors = []

    result = dict(
        changed=False,
        original_message="",
        message=""
    )

    state = module.params["state"]
    a10_host = module.params["a10_host"]
    a10_username = module.params["a10_username"]
    a10_password = module.params["a10_password"]
    # TODO(remove hardcoded port #)
    a10_port = 443
    a10_protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        map(run_errors.append, validation_errors)
    
    if not valid:
        result["messages"] = "Validation failure"
        err_msg = "\n".join(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(a10_host, a10_port, a10_protocol, a10_username, a10_password)

    if state == 'present':
        result = present(module, result)
    elif state == 'absent':
        result = absent(module, result)
    return result

def main():
    module = AnsibleModule(argument_spec=get_argspec())
    result = run_command(module)
    module.exit_json(**result)

# standard ansible module imports
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()