import schedule_helper as sch_help
import schedule_query as sch_query
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--list-schedules", "--get-schedules", "-ls",
        help="print compatible schedules",
        action="store_true"
    )
    parser.add_argument(
        "--query", "-q",
        help="go directly into query mode",
        action="store_true"
    )
    parser.add_argument(
        "--open-with", "--open", "-o",
        help="open with specified program"
    )
    parser.add_argument(
        "--schedule", "--sch", "-s",
        help="uses the provided .txt file for schedule (default: schedules.txt)"
    )
    args = parser.parse_args()

    file = "schedules.txt"
    if args.schedule:
        file = args.schedule

    schedules = sch_help.get_schedule_as_dict(file)
    comb_list, comb_tuple = sch_help.get_compatible_combinations(schedules)

    if args.list_schedules:
        sch_help.main_print_schedules(schedules, comb_list, comb_tuple)
    elif args.query:
        sch_query.wildcard_query_multiple(comb_list, comb_tuple)
    elif args.open_with:
        print("Opening output with", args.open_with)
        success = sch_query.main_schedule_query(schedules, comb_list, comb_tuple)
        if success:
            sch_query.open_excel_sheet(program=args.open_with)
    else:
        sch_query.main_schedule_query(schedules, comb_list, comb_tuple)
