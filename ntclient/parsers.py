import os

from .services import _init
from .services.analyze import day_analyze, foods_analyze
from .services.recipe import (
    recipe_add as _recipe_add,
    recipe_edit as _recipe_edit,
    recipe_overview,
    recipes_overview,
)
from .services.biometrics import (
    biometrics,
    biometric_add,
    biometric_logs,
)
from .services.usda import (
    list_nutrients,
    search_results,
    sort_foods_by_kcal_nutrient_id,
    sort_foods_by_nutrient_id,
)


def init(args, arg_parser=None, **kwargs):
    _init()


# --------------------------
# Nutrients, search and sort
# --------------------------
def nutrients(args, arg_parser=None, **kwargs):
    return list_nutrients()


def search(args, arg_parser=None, subparsers=None):
    """ Searches all dbs, foods, recipes, recents and favorites. """
    if args.terms:
        return search_results(words=args.terms)
    else:
        subparsers["search"].print_help()


def sort(args, arg_parser=None, subparsers=None):
    nutr_id = args.nutr_id
    if not nutr_id:
        subparsers["sort"].print_help()
    elif args.kcal:
        return sort_foods_by_kcal_nutrient_id(nutr_id)
    else:
        return sort_foods_by_nutrient_id(nutr_id)


# --------------------------
# Analysis and Day scoring
# --------------------------
def analyze(args, arg_parser=None, subparsers=None):
    food_ids = args.food_id
    grams = args.grams

    if not food_ids:
        subparsers["anl"].print_help()
    else:
        return foods_analyze(food_ids, grams)


def day(args, arg_parser=None, subparsers=None):
    day_csv_paths = args.food_log
    day_csv_paths = [os.path.expanduser(x) for x in day_csv_paths]
    if args.rda:
        rda_csv_path = os.path.expanduser(args.rda)

    if not day_csv_paths:
        subparsers["day"].print_help()
    elif not args.rda:
        return day_analyze(day_csv_paths)
    else:
        return day_analyze(day_csv_paths, rda_csv_path=rda_csv_path)


# --------------------------
# Biometrics
# --------------------------
def bio(args, arg_parser=None, subparsers=None):
    return biometrics()


def bio_log(args, arg_parser=None, subparsers=None):
    return biometric_logs()


def bio_log_add(args, arg_parser=None, subparsers=None):
    bio_vals = {
        int(x.split(",")[0]): float(x.split(",")[1]) for x in args.biometric_val
    }

    return biometric_add(bio_vals)


# --------------------------
# Recipes
# --------------------------
def recipe(args, arg_parser=None, subparsers=None):
    if args.recipe_id:
        return recipe_overview(args.recipe_id)
    else:
        return recipes_overview()


def recipe_add(args, arg_parser=None, subparsers=None):
    food_amts = {int(x.split(",")[0]): float(x.split(",")[1]) for x in args.food_amt}
    return _recipe_add(args.name, food_amts)


def recipe_edit(args, arg_parser=None, subparsers=None):
    return _recipe_edit(args.recipe_id)


# --------------------------
# Sync
# --------------------------
def sync(args, arg_parser=None, subparsers=None):
    from .services.sync import sync as _sync

    _sync()


def sync_register(args, arg_parser=None, subparsers=None):
    from getpass import getpass
    from .services.sync import register

    print("not implemented ;]")
    return

    email = input("email: ")
    confirm_email = input("confirm email: ")
    password = getpass("password: ")
    confirm_password = getpass("confirm password: ")

    if email != confirm_email or password != confirm_password:
        print("Try again, email and password must match")
        return

    register(email, password)


def sync_login(args, arg_parser=None, subparsers=None):
    from getpass import getpass
    from .services.sync import login

    password = getpass("password: ")
    login(args.email, password)
