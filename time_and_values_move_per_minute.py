# from Classes import time_local_time
# import time
#
#
# def make_lists():
#     lst_time = []
#     lst_value = []
#     lst_result = []
#
#     for counter in range(0, 60):
#         if len(str(counter)) == 1:
#             lst_time.append("14:0" + str(counter))
#         else:
#             lst_time.append("14:" + str(counter))
#         lst_value.append(counter)
#
#     for counter in range(0, 60):
#         if len(str(counter)) == 1:
#             lst_time.append("15:0" + str(counter))
#         else:
#             lst_time.append("15:" + str(counter))
#         lst_value.append(counter)
#
#     lst_time.append("16:00")
#     lst_value.append(60)
#     lst_result.append(lst_time)
#     lst_result.append(lst_value)
#     return lst_result
#
#
# try:  # main programme
#     # make simulation lists
#     lst_data = make_lists()
#     lst_time = lst_data[0]
#     lst_value = lst_data[1]
#
#     # get time
#     time_now = time_local_time.time_local_time().get_local_time()
#     print(time_now)
#     while True:
#         if time_now != time_local_time.time_local_time().get_local_time():  # check if minute has passed
#             time_now = time_local_time.time_local_time().get_local_time()  # save time at this moment
#
#             print("\nTijd: %s" % time_now)  # show time now
#
#             for index in range(0, len(lst_time)):  # go trough list
#                 if lst_time[index] == time_now:  # search for time in list that is equal to the time now
#                     # create effect where value of now is always in middle of graph
#                     lst_min = index - 29  # show 29 values before
#                     lst_max = index + 30  # show 30 values after
#
#             # print result
#             print("Tijden ervoor en erna: %s" % lst_time[lst_min:lst_max])
#             print("Waarden ervoor en erna: %s" % lst_value[lst_min:lst_max])
#
# except KeyboardInterrupt:
#     pass

from Classes import time_local_time
import time

try:  # main programme
    time_now = time_local_time.time_local_time().get_local_time()  # get time

    while True:
        if time_now != time_local_time.time_local_time().get_local_time():  # check if minute has passed
            time_now = time_local_time.time_local_time().get_local_time()  # save time at this moment

            for index in range(0, len(lst_time)):  # go trough list
                if lst_time[index] == time_now:  # search for time in list that is equal to the time now
                    # create effect where value of now is always in middle of graph
                    lst_min = index - 29  # show 29 values before
                    lst_max = index + 30  # show 30 values after

except KeyboardInterrupt:
    pass

