#!/usr/bin/env python3

import os
import yaml

onu_path_templ = "docs/{0}/ont/{1}/{2}.md"
device_templ = "{{% extends \"{0}\" %}}\n{{% set onu_type = {1} %}}\n{{% set device = onu_type.{2} %}}"

class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def generate_vendors_lists(device_list):
    list = {}
    for id, device in device_list:
        vendor = device.get('vendor')
        list[vendor] = []
    return list

def iterate_device_list(device_list):
    list = {}
    for id, device in device_list:
        dev = {}

        vendor = device.get('vendor')
        odm = device.get('odm')
        title = device.get('title')
        aliases = device.get('aliases')
        template = device.get('template')

        dev['id'] = id
        dev['vendor'] = vendor
        dev['title'] = title

        if odm != None:
            dev['odm'] = odm

        if aliases != None and template != None:
            dev['aliases'] = aliases
            dev['template'] = template

        list[id] = dev

    return list

def get_device_info(device):
    return (device['id'], device['vendor'], device['title'])

def write_file(filename, contents):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as file:
        file.write(contents)
    return

def create_file(device, type='gpon', other=None):
    if other != None:
        id, vendor, title = get_device_info(other)
    else:
        id, vendor, title = get_device_info(device)

    template = device.get('template', "device.tmpl")
    filename = onu_path_templ.format(type, vendor, id)
    write_file(filename, device_templ.format(template, type + "_onu", id))

    return { title: filename[5:] }

def process_devices_file(filename):
    with open(filename, 'r') as onu_file:
        devices = yaml.safe_load(onu_file)
    
    nav = []

    if devices != None:
        if "xgs_pon" in filename:
            type = 'xgs_pon'
        else:
            type = 'gpon'
        onu_list = iterate_device_list(devices.items())
        nav_items = generate_vendors_lists(devices.items())

        for _,onu in onu_list.items():
            if onu.get('odm') == None:
                item = create_file(onu, type)
                nav_items[onu['vendor']].append(item)
                
            if onu.get('aliases') != None:
                for alias in onu['aliases']:
                    item = create_file(onu, type, onu_list[alias])
                    nav_items[onu_list[alias]['vendor']].append(item)

        for key,value in nav_items.items():
            nav.append({key: sorted(value, key=lambda d: list(d.keys()))})

    if 'gpon' in filename:
        return { 'GPON': ['gpon/index.md', { 'ONT': sorted(nav, key=lambda d: list(d.keys())) }] }
    elif 'xgs_pon' in filename:
        return { 'XGS-PON': ['xgs_pon/index.md', { 'ONT': sorted(nav, key=lambda d: list(d.keys())) }] }
    else:
        return None

def main():
    with open('mkdocs.yml', 'r') as mkdocs_file:
        mkdocs = yaml.safe_load(mkdocs_file)
        
    if mkdocs != None:
        file_list = []

        tmp_list = [item for item in mkdocs['plugins'] if isinstance(item, dict) and item.get('macros') != None]

        for macros_dict in tmp_list:
            for option,value_list in macros_dict['macros'].items():
                if option == 'include_yaml':
                    for value in value_list:
                        if isinstance(value, dict): 
                            for _,path in value.items():
                                file_list.append(path)
                        elif isinstance(value, str):
                            file_list.append(value)
        nav_list = []

        for filename in [name for name in file_list if '_onu' in name]:
            nav_list.append(process_devices_file(filename))

        nav_list = sorted(nav_list, key=lambda d: list(d.keys()))
        nav_list.insert(0, {'Home': 'index.md'})
        mkdocs['nav'] = nav_list

        with open('mkdocs.yml', 'w') as mkdocs_file:
            yaml.dump(mkdocs, mkdocs_file, sort_keys=False, Dumper=NoAliasDumper)

    return

if __name__ == '__main__':
    main()
