"""
    Sample JSON [meta data] utils
"""
import argparse
import eager.libs.utils as utils


def get_args_merge():
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--json-file", type=str, required=True,
                    help='json files to be merged', nargs='+')
    ap.add_argument("-o", "--outfile", type=str, required=True,
                    help='file to hold the result')
    args, _ = ap.parse_known_args()
    return vars(args)


def get_args_clean():
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--json-file", type=str, required=True,
                    help='json files to be merged')
    ap.add_argument("-o", "--outfile", type=str, required=True,
                    help='file to hold the result')
    args, _ = ap.parse_known_args()
    return vars(args)


def merge():
    args = get_args_merge()
    jsons = []
    for j in args["json_file"]:
        jsons.extend(utils.open_json(j))
    utils.save_json(jsons, args["outfile"])


def clean():
    args = get_args_clean()
    import os
    full_path = os.path.abspath(args["json_file"])
    folder = os.path.dirname(full_path)
    all_imgs = utils.open_json(args["json_file"])
    filtered = utils.filter_by_type(os.listdir(folder), "_c.jpg")

    clean_json = []
    for img in all_imgs:
        for one in filtered:
            if utils.equal(img["file_name"], one):
                clean_json.append(img)
                break

    utils.save_json(clean_json, args["outfile"])


def run():
    ap = argparse.ArgumentParser(
        description="Module for actions on metadata JSON files, choose one:")
    ap.add_argument("function", choices=["merge", "clean"])
    args, _ = ap.parse_known_args()

    if args.function == "merge":
        merge()
    elif args.function == "clean":
        clean()
if __name__ == "__main__":
    run()
