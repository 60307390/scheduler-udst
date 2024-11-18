import schedule_helper as sch_help
import schedule_query as sch_query
import argparse

if __name__ == "__main__":
    schedules = sch_help.get_schedule_as_dict()
    comb_list, comb_tuple = sch_help.get_compatible_combinations(schedules)
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--list-schedules", "--get-schedules", "-ls",
        help = "print compatible schedules",
        action="store_true"
    )
    parser.add_argument(
        "--query", "-q",
        help = "go directly into query mode",
        action="store_true"
    )
    args = parser.parse_args()

    if args.list_schedules:
        sch_help.main_print_schedules(schedules, comb_list, comb_tuple)
    elif args.query:
        sch_query.wildcard_query_multiple(comb_list, comb_tuple)
    else:
        sch_query.main_schedule_query(schedules, comb_list, comb_tuple)