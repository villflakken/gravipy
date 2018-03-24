def timeprint(totsecs):
    """
    Takes integer/float input: an amount of time (in seconds),
    returns string of hours, minutes, seconds.
    """   
    timestring = "{h:1d}h, {m:1d}m, {s:1d}s"
    seconds_in_an_hour  = 3600.
    seconds_in_a_minute = 60.
    hours   =  totsecs // seconds_in_an_hour
    minutes = (totsecs %  seconds_in_an_hour) // seconds_in_a_minute
    seconds = (totsecs %  seconds_in_an_hour) %  seconds_in_a_minute
    return  timestring.format(h=hours, m=minutes, s=seconds)