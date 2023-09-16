#!/usr/bin/env python3

import os
import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open('include/vendors.yml', "r") as vendors_file:
    vendors = yaml.safe_load(vendors_file)

onu_path_templ = "docs/{0}/ont/{1}/{2}.md"
device_templ = '{{% extends "{0}" %}}\n{{% set onu_type = {1} %}}\n{{% set device = onu_type.{2} %}}'

def generate_vendors_lists(device_list):
    list = {}
    for _, device in device_list:
        vendor_name = device.get("vendor")
        
        if vendors.get(vendor_name):
            if vendors[vendor_name].get("short_title"):
                list[vendors[vendor_name]["short_title"]] = []
            else:
                list[vendors[vendor_name]["title"]] = []
    return list


def iterate_device_list(device_list):
    list = {}
    for id, device in device_list:
        dev = {}

        vendor = device.get("vendor")
        odm = device.get("odm")
        title = device.get("title")
        aliases = device.get("aliases")
        template = device.get("template")

        dev["id"] = id
        dev["vendor"] = vendor
        dev["title"] = title

        if odm:
            dev["odm"] = odm
        if aliases:
            dev["aliases"] = aliases
        if template:
            dev["template"] = template

        list[id] = dev

    return list


def get_device_info(device):
    return (device["id"], device["vendor"], device["title"])


def write_file(filename, contents):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as file:
        file.write(contents)
    return


def create_file(device, type={"system":"gpon", "device":"onu"}, other=None):
    odm = None

    if other:
        id, vendor, title = get_device_info(other)
        odm = other.get("odm")
        if odm:
            template = other.get("template", "odm.tmpl")
        else:
            template = other.get("template", "device.tmpl")
    else:
        id, vendor, title = get_device_info(device)
        if device.get("aliases"):
            odm = device
            template = device.get("template", "odm.tmpl")
        else:
            template = device.get("template", "device.tmpl")
 
    filename = onu_path_templ.format(
        type["system"].replace("_", "-").lower(), vendor.lower(), id.replace("_", "-")
    )
    write_file(filename, device_templ.format(template, type["system"] + "_" + type["device"], id))

    return {title: filename[5:]}


def process_devices_file(filename):
    with open(filename, "r") as onu_file:
        devices = yaml.safe_load(onu_file)

    nav = []
    type = {}

    if devices:
        if "xgs_pon" in filename:
            type["system"] = "xgs_pon"
        elif "gpon" in filename:
            type["system"] = "gpon"
        elif "epon" in filename:
            type["system"] = "epon"
        elif "10g_epon" in filename:
            type["system"] = "10g_epon"
        else:
            return
        
        if "_onu" in filename:
            type["device"] = "ont"
        elif "_olt" in filename:
            type["device"] = "olt"
        else:
            return

        onu_list = iterate_device_list(devices.items())
        nav_items = generate_vendors_lists(devices.items())

        for _, onu in onu_list.items():
            if not onu.get("odm"):
                item = create_file(onu, type)
                nav_items[vendors[onu["vendor"]]["title"]].append(item)

            if onu.get("aliases"):
                for alias in onu["aliases"]:
                    item = create_file(onu, type, onu_list[alias])
                    if vendors[onu_list[alias]["vendor"]].get("short_title"):
                        nav_items[vendors[onu_list[alias]["vendor"]]["short_title"]].append(item)
                    else:
                        nav_items[vendors[onu_list[alias]["vendor"]]["title"]].append(item)

        for key, value in nav_items.items():
            nav.append({key: sorted(value, key=lambda d: list(d.keys()))})

        if type["device"] == "olt":
            return (type, {"OLT": sorted(nav, key=lambda d: list(d.keys()))})
        elif type["device"] == "ont":
            return (type, {"ONT": sorted(nav, key=lambda d: list(d.keys()))})

    return None


def main():
    with open("mkdocs.yml", "r") as mkdocs_file:
        mkdocs = yaml.load(mkdocs_file, Loader=Loader)

    if mkdocs:
        file_list = []

        tmp_list = [
            item
            for item in mkdocs["plugins"]
            if isinstance(item, dict) and item.get("macros")
        ]

        for macros_dict in tmp_list:
            for option, value_list in macros_dict["macros"].items():
                if option == "include_yaml":
                    for value in value_list:
                        if isinstance(value, dict):
                            for _, path in value.items():
                                file_list.append(path)
                        elif isinstance(value, str):
                            file_list.append(value)
        nav_list = []

        for filename in [
            name for name in file_list if "_onu" in name or "_olt" in name
        ]:
            nav_list.append(process_devices_file(filename))

        nav_list = sorted(nav_list, key=lambda d: list(d[1].keys()))

        nav = mkdocs["nav"]
        for type, tree in nav_list:
            type_index = next((index for (index, d) in enumerate(nav) if d.get(type["system"].replace("_", "-").upper()) != None), None)
            if type_index:
                nav_type = enumerate(nav[type_index][type["system"].replace("_", "-").upper()])
                device_index = next((index for (index, d) in nav_type if isinstance(d, dict) and d.get(type["device"].upper()) != None), None)
                if device_index:
                    nav[type_index][type["system"].replace("_", "-").upper()][device_index] = tree
                else:
                    nav[type_index][type["system"].replace("_", "-").upper()].append(tree)

        with open("mkdocs.yml", "w") as mkdocs_file:
            yaml.dump(mkdocs, mkdocs_file, sort_keys=False, Dumper=Dumper)

    return


if __name__ == "__main__":
    main()
