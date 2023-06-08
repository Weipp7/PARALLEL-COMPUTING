import os, re
import matplotlib.pyplot as plt

thread_runtime = [0] * 17
serial_runtime = [0] * 17
speedup = [0] * 17
thread_num = [x for x in range(17)]
for i in range(2, 17):
    printinfo = os.popen(
        "~/OI/parallel_computing/program1/asst1/prog1_mandelbrot_threads/mandelbrot -t %d -v 2"
        % i
    ).read()
    # print(printinfo)
    thread_runtime[i] = float(
        re.findall(r"\[mandelbrot thread\]:.+\[([-+]?[0-9]*\.?[0-9]+)\]", printinfo)[0]
    )
    serial_runtime[i] = float(
        re.findall(r"\[mandelbrot serial\]:.+\[([-+]?[0-9]*\.?[0-9]+)\]", printinfo)[0]
    )
    speedup[i] = round(serial_runtime[i] / thread_runtime[i], 2)
    print(speedup[i])
print(thread_runtime)

plt.subplot(1, 2, 1)
l1 = plt.plot(thread_num[2:], thread_runtime[2:], "b--", label="runtime")
plt.plot(thread_num[2:], thread_runtime[2:], "bo-")
# plt.title("The runtime in Parallel Computing")
plt.ylabel("thread_runtime")
plt.xlabel("thread_num")
plt.legend()

plt.subplot(1, 2, 2)
l1 = plt.plot(thread_num[2:], speedup[2:], "r--", label="speed up")
plt.plot(thread_num[2:], speedup[2:], "ro-")
# plt.title("The Speed Up in Parallel Computing")
plt.ylabel("speed_up")
plt.xlabel("thread_num")
plt.legend()

plt.suptitle("The Runtime and Speed Up in Parallel Computing")
plt.savefig("./v2_after optimization.jpg")
plt.show()
