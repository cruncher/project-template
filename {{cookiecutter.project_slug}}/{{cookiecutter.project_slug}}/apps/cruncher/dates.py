def time_range(start_date, end_date, separator):
    if start_date and end_date:
        if end_date > start_date:
            start_strf = "%d"
            if end_date.month != start_date.month:
                start_strf += ".%m"
            if end_date.year != start_date.year:
                start_strf += ".%Y"

            start_date_ = start_date.strftime(start_strf)
            end_date_ = end_date.strftime("%d.%m.%Y")

            return f"{start_date_}{separator}{end_date_}"

        else:
            return start_date.strftime("%d.%m.%Y")
    elif start_date:
        return start_date.strftime("%d.%m.%Y")
    elif end_date:
        return end_date.strftime("%d.%m.%Y")
