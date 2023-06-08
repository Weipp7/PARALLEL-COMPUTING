## 针对Program3的分析

### Part Ⅰ

从理论上讲，我们可以期望最大加速比为 8，即相较于串行代码，使用 ISPC 实现的并行化代码应该能够达到 8 倍的性能提升。

然而，实际观察到的加速比(4.77x speedup from ISPC)低于这个理想值，原因可能如下：

1. 数据依赖性：尽管每个像素的计算是独立的，但在每个像素的计算过程中，存在数据依赖性。具体来说，后续迭代中的计算依赖于前面迭代的结果，即 `z_re`和 `z_im`的值。这种数据依赖性限制了并行计算的能力，导致并行化效果受到限制。

2. 数据访问模式：在计算过程中，`z_re`和 `z_im`的值在每个迭代中都被更新，这可能导致不规则的内存访问模式。这种非连续的数据访问模式对于并行化和向量化优化可能不利，降低了性能。

3. 分支和条件语句：在 `mandel`函数中，存在一个条件判断语句，即判断 `z_re * z_re + z_im * z_im > 4.f`。这种条件判断语句可能导致分支的发生，而分支对于并行化和向量化优化来说是具有挑战性的。分支会导致不同线程执行不同的代码路径，从而影响并行化的效果。

### Part Ⅱ

#### 1. `mandelbrot_ispc`带参数运行 `--tasks`

```c
weipp7@LAPTOP-OCJ7S5SF:~/OI/parallel_computing/program1/asst1/prog3_mandelbrot_ispc$ ./mandelbrot_ispc --tasks
[mandelbrot serial]:            [242.826] ms
Wrote image file mandelbrot-serial.ppm
[mandelbrot ispc]:              [46.897] ms
Wrote image file mandelbrot-ispc.ppm
[mandelbrot multicore ispc]:    [11.552] ms
Wrote image file mandelbrot-task-ispc.ppm
                                (5.18x speedup from ISPC)
                                (21.02x speedup from task ISPC)
```

#### 2. 修改任务数提高性能

根据给定的代码和描述，我们可以看到 `mandelbrot_ispc_withtasks`函数将图像的高度分为 `rowsPerTask`行，并将任务数设置为 `height/rowsPerTask`。根据给定的行数，该实现将创建相应数量的任务，每个任务处理一组连续的行。

要选择最佳的任务数，我们可以进行一些实验和基准测试，以确定哪个任务数提供了最好的性能。我们可以尝试使用不同的任务数，并根据每个任务的计算负载和总执行时间来评估性能。根据实验结果，选择任务数可以使计算负载相对均衡，并在给定硬件上实现最佳性能。

在尝试了2，4，8，16，32等一组数字后，发现任务数为32时能够得到32倍以上的性能。

```c
weipp7@LAPTOP-OCJ7S5SF:~/OI/parallel_computing/program1/asst1/prog3_mandelbrot_ispc$ ./mandelbrot_ispc --tasks
[mandelbrot serial]:            [231.770] ms
Wrote image file mandelbrot-serial.ppm
[mandelbrot ispc]:              [43.611] ms
Wrote image file mandelbrot-ispc.ppm
[mandelbrot multicore ispc]:    [7.370] ms
Wrote image file mandelbrot-task-ispc.ppm
                                (5.31x speedup from ISPC)
                                (32.45x speedup from task ISPC)
```

原因如下：

* 负载均衡：任务数的选择需要考虑计算负载的均衡性。如果任务数过少，每个任务可能会处理较大的计算量，导致负载不平衡。相反，如果任务数过多，每个任务的计算量可能会变得较小，导致任务间的通信和调度开销增加。选择32个任务可能是在给定硬件和图像大小的情况下实现了较好的负载均衡，使每个任务的计算量相对均匀。
* SIMD并行性：ISPC的优势在于利用SIMD指令进行并行计算。选择32个任务可能与硬件的SIMD宽度相匹配，因此每个任务可以充分利用向量化指令。这意味着在每个任务中，计算能够以SIMD方式并行执行，从而实现更高的计算效率。

#### 3.线程抽象和ISPC任务抽象

线程抽象是传统的多线程编程模型，在多线程编程中，程序会创建多个线程，每个线程都有自己的执行上下文和调度。线程抽象允许开发者在并发环境中以相对较小的粒度执行任务。在程序中，使用线程抽象（如create/join机制）时，当创建10000个线程时，会导致系统为每个线程分配资源（如堆栈空间、寄存器状态等），并进行线程调度和上下文切换，这会导致系统开销增加。

ISPC任务抽象是针对数据并行任务设计的一种抽象机制，它利用SIMD指令进行向量化计算。在ISPC任务抽象中，任务被划分为多个程序实例，这些实例可以在SIMD处理器上并行执行。ISPC的任务模型更适用于数据并行任务，它利用SIMD并行性和向量化指令来提高计算效率。

在一般情况下，当启动10000个线程时，会因为线程管理和调度的开销而导致系统性能下降，而启动10000个ISPC任务时，这些任务会被分配给SIMD处理器进行并行执行，而不需要线程的创建和管理。这会充分利用硬件的并行计算能力，通过SIMD并行和向量化指令来提高计算效率。因此，ISPC任务抽象在处理数据并行任务时通常比线程抽象更具优势。
