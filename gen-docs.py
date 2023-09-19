#!/usr/bin/env python3

import os
import yaml
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("include/vendors.yml", "r") as vendors_file:
    vendors = yaml.safe_load(vendors_file)

onu_path_templ = "docs/{0}/{3}/{1}/{2}.md"
device_templ = '{{% extends "{0}" %}}\n{{% set {3}_type = {1}_{3} %}}\n{{% set device = {3}_type.{2} %}}'


def generate_vendors_lists(device_list):
    list = {}
    for _, device in device_list:
        vendor = device.get("vendor")

        if not vendors.get(vendor):
            continue

        if vendors[vendor].get("short_title"):
            list[vendors[vendor]["short_title"]] = []
        else:
            list[vendors[vendor]["title"]] = []

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


def create_file(device, pon, other=None):
    odm = None

    if pon == None:
        return None

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
        pon["type"].replace("_", "-").lower(),
        vendor.lower(),
        id.replace("_", "-"),
        pon["device"],
    )

    write_file(filename, device_templ.format(template, pon["type"], id, pon["device"]))

    return {title: filename[5:]}


def get_pon(filename):
    pon = {}
    if "xgs_pon" in filename:
        pon["type"] = "xgs_pon"

    elif "gpon" in filename:
        pon["type"] = "gpon"

    elif "epon" in filename:
        pon["type"] = "epon"

    elif "10g_epon" in filename:
        pon["type"] = "10g_epon"

    else:
        return None

    if "_onu" in filename:
        pon["device"] = "onu"

    elif "_olt" in filename:
        pon["device"] = "olt"

    else:
        return None

    return pon


def process_devices_file(filename, pon):
    with open(filename, "r") as onu_file:
        devices = yaml.safe_load(onu_file)

    nav = []

    if not devices or not pon:
        return None

    onu_list = iterate_device_list(devices.items())
    nav_items = generate_vendors_lists(devices.items())

    for _, onu in onu_list.items():
        if onu.get("odm"):
            continue

        vendor = vendors[onu["vendor"]]
        item = create_file(onu, pon)

        if item == None:
            print("Error creating file for " + pon + " device " + onu )
            continue

        if vendor.get("short_title"):
            nav_items[vendor["short_title"]].append(item)
        else:
            nav_items[vendor["title"]].append(item)

        if not onu.get("aliases"):
            continue

        for alias in onu["aliases"]:
            vendor = vendors[onu_list[alias]["vendor"]]
            item = create_file(onu, pon, onu_list[alias])

            if item == None:
                return None

            if vendor.get("short_title"):
                nav_items[vendor["short_title"]].append(item)
            else:
                nav_items[vendor["title"]].append(item)

    for key, value in nav_items.items():
        nav.append({key: sorted(value, key=lambda d: list(d.keys()))})

    return (
        pon,
        {pon["device"].upper(): sorted(nav, key=lambda d: list(d.keys()))},
    )


def get_nav_indices(nav):
    nav_enumeration = enumerate(nav)
    home_index = next(
        (index for (index, d) in nav_enumeration if d.get("Home") != None),
        None,
    )
    teng_epon_index = next(
        (index for (index, d) in nav_enumeration if d.get("10G-EPON") != None),
        None,
    )
    epon_index = next(
        (index for (index, d) in nav_enumeration if d.get("EPON") != None),
        None,
    )
    gpon_index = next(
        (index for (index, d) in nav_enumeration if d.get("GPON") != None),
        None,
    )
    xgs_pon_index = next(
        (index for (index, d) in nav_enumeration if d.get("XGS-PON") != None),
        None,
    )

    return {
        "Home": home_index,
        "10G-EPON": teng_epon_index,
        "EPON": epon_index,
        "GPON": gpon_index,
        "XGS-PON": xgs_pon_index,
    }


def nav_insert(nav, indices, pon_type):
    if pon_type == "10G-EPON":
        nav.insert(indices.get("Home") + 1, {"10G-EPON": ["10g-epon/index.md"]})

    elif pon_type == "EPON":
        epon = {"EPON": ["epon/index.md"]}

        if indices.get("10G-EPON"):
            nav.insert(indices.get("10G-EPON") + 1, epon)
        else:
            nav.insert(indices.get("Home") + 1, epon)

    elif pon_type == "GPON":
        gpon = {"GPON": ["gpon/index.md"]}

        if indices.get("XGS-PON"):
            nav.insert(indices.get("XGS-PON"), gpon)
        else:
            nav.append(gpon)

    elif pon_type == "XGS-PON":
        nav.append({"XGS-PON": ["xgs-pon/index.md"]})

    return nav


def main():
    with open("mkdocs.yml", "r") as mkdocs_file:
        mkdocs = yaml.load(mkdocs_file, Loader=Loader)

    if not mkdocs:
        return

    macros_index = next(
        (
            index
            for (index, d) in enumerate(mkdocs["plugins"])
            if isinstance(d, dict) and d.get("macros") != None
        ),
        None,
    )

    if not macros_index:
        return
    
    file_list = []

    for option, value_list in mkdocs["plugins"][macros_index]["macros"].items():
        if option != "include_yaml":
            continue

        for value in value_list:
            if isinstance(value, dict):
                for _, path in value.items():
                    file_list.append(path)

            elif isinstance(value, str):
                file_list.append(value)
        break

    nav_groups = []

    for filename in [name for name in file_list if get_pon(name) != None]:
        nav_groups.append(process_devices_file(filename, get_pon(filename)))

    nav_groups = sorted(nav_groups, key=lambda d: list(d[1].keys()))

    nav = mkdocs["nav"]

    indices = get_nav_indices(nav)

    for pon, nav_group in nav_groups:
        pon_type = pon["type"].replace("_", "-").upper()
        pon_device = pon["device"].upper()
        pon_index = indices.get(pon_type)

        if pon_index == None:
            nav = nav_insert(nav, indices, pon_type)
            indices = get_nav_indices(nav)
            pon_index = indices.get(pon_type)

        device_index = next(
            (
                index
                for (index, d) in enumerate(nav[pon_index][pon_type])
                if isinstance(d, dict) and d.get(pon_device) != None
            ),
            None,
        )

        if device_index:
            nav[pon_index][pon_type][device_index] = nav_group
            continue

        dicts = [item for item in nav[pon_index][pon_type] if isinstance(item, dict)]
        strings = [item for item in nav[pon_index][pon_type] if isinstance(item, str)]

        dicts.append(nav_group)
        nav[pon_index][pon_type] = strings + sorted(dicts, key=lambda d: list(d.keys()))

    with open("mkdocs.yml", "w") as mkdocs_file:
        yaml.dump(mkdocs, mkdocs_file, sort_keys=False, Dumper=Dumper)

    return


if __name__ == "__main__":
    main()
