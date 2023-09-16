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
    for id, device in device_list:
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


def create_file(device, type="gpon", other=None):
    odm = None
    
    if other:
        id, vendor, title = get_device_info(other)
        odm = other.get("odm")
    else:
        id, vendor, title = get_device_info(device)
        if device.get("aliases"):
            odm = device

    if odm:
        template = device.get("template", "odm.tmpl")
    else:
        template = device.get("template", "device.tmpl")
 
    filename = onu_path_templ.format(
        type.replace("_", "-").lower(), vendor.lower(), id.replace("_", "-")
    )
    write_file(filename, device_templ.format(template, type + "_onu", id))

    return {title: filename[5:]}


def process_devices_file(filename):
    with open(filename, "r") as onu_file:
        devices = yaml.safe_load(onu_file)

    nav = []

    if devices != None:
        if "xgs_pon" in filename:
            type = "xgs_pon"
        elif "gpon" in filename:
            type = "gpon"
        elif "epon" in filename:
            type = "epon"
        elif "10g_epon" in filename:
            type = "10g_epon"
        else:
            return

        onu_list = iterate_device_list(devices.items())
        nav_items = generate_vendors_lists(devices.items())

        for _, onu in onu_list.items():
            if onu.get("odm") == None:
                item = create_file(onu, type)
                nav_items[vendors[onu["vendor"]]["title"]].append(item)

            if onu.get("aliases") != None:
                for alias in onu["aliases"]:
                    item = create_file(onu, type, onu_list[alias])
                    if vendors[onu_list[alias]["vendor"]].get("short_title"):
                        nav_items[vendors[onu_list[alias]["vendor"]]["short_title"]].append(item)
                    else:
                        nav_items[vendors[onu_list[alias]["vendor"]]["title"]].append(item)

        for key, value in nav_items.items():
            nav.append({key: sorted(value, key=lambda d: list(d.keys()))})

        return {
            type.replace("_", "-").upper(): [
                type.replace("_", "-").lower() + "/index.md",
                {"ONT": sorted(nav, key=lambda d: list(d.keys()))},
            ]
        }

    return None


def main():
    with open("mkdocs.yml", "r") as mkdocs_file:
        mkdocs = yaml.load(mkdocs_file, Loader=Loader)

    if mkdocs != None:
        file_list = []

        tmp_list = [
            item
            for item in mkdocs["plugins"]
            if isinstance(item, dict) and item.get("macros") != None
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

        nav_list = sorted(nav_list, key=lambda d: list(d.keys()))
        nav_list.insert(0, {"Home": "index.md"})
        mkdocs["nav"] = nav_list

        with open("mkdocs.yml", "w") as mkdocs_file:
            yaml.dump(mkdocs, mkdocs_file, sort_keys=False, Dumper=Dumper)

    return


if __name__ == "__main__":
    main()
