## 针对Program4的分析

### 1. 运行sqrt

无任务加速： 4.44

有任务加速： 31.33

```c
weipp7@LAPTOP-OCJ7S5SF:~/OI/parallel_computing/program1/asst1/prog4_sqrt$ ./sqrt 
[sqrt serial]:          [871.189] ms
[sqrt ispc]:            [196.332] ms
[sqrt task ispc]:       [27.808] ms
                                (4.44x speedup from ISPC)
                                (31.33x speedup from task ISPC)
```

### 2. 修改输入使加速最大化

当修改如下输入可以得到最大的加速比：

```cpp
values[i] = 2.999999f;
```

(6.33x speedup from ISPC) 

(56.36x speedup from task ISPC)

即将初始猜测设置为远离精确解的值会让加速比显著提高。

原因是在没有任务并行化的情况下，即单线程执行ISPC程序，每个计算任务都是按顺序执行的。由于这是一个迭代的平方根计算过程，需要多次迭代才能收敛到精确解。当初始猜测不准确时，需要更多的迭代次数才能收敛。因此，当将初始输入设置为 `values[i] = 2.999999f;`时，程序执行的迭代次数增加，导致运行时间延长，加速比相对较低。

而有任务并行化的ISPC程序可以将任务分配给多个并行实例，在不同的并行实例上并行执行迭代计算。当初始输入设置为远离精确解的值时，不同的任务会更快地收敛到精确解。这样，有任务并行化的ISPC程序可以更快地完成迭代计算，从而显著提高了加速比。

有任务并行化相比无任务并行化的好处包括：

1. 提高了计算速度：有任务并行化能够将计算任务并行执行，利用多个处理单元或多个核心同时进行计算，从而加快了整体计算速度。
2. 更高的利用率：有任务并行化能够充分利用硬件资源，将计算任务分配给多个并行实例执行，使得计算资源得到更充分的利用，提高了系统的效率。
3. 提升响应能力：有任务并行化可以提高系统的响应能力，能够同时处理多个任务，减少了任务的等待时间，从而提升了系统的整体性能。

### 3. 修改输入使无任务并行加速最小化

当修改如下输入可以得到最小的加速比：

```cpp
values[i] = 1.f;
```

1.74x speedup from ISPC

在这个输入中，每个值的平方根都非常接近初始猜测1.0，因此迭代的次数相对较少。通过这种方式，我们减小了迭代计算的工作负载，并限制了并行计算的效益。

选择这个输入的原因是，它使得每个任务的计算时间几乎相同，并且任务之间没有明显的工作不平衡。这导致并行执行的任务无法充分利用并行计算的优势，因为任务之间没有足够的计算差异来提高整体性能。

相对于顺序版本的性能，sqrtISPC（无任务）在这个特定输入上的加速比将非常接近于1，即几乎没有加速。这是因为并行计算的开销超过了并行化带来的好处。并行计算的开销包括任务划分、任务调度、同步等，而在这个输入中，每个任务的计算时间非常短，导致并行计算的开销占据了主要部分，而并行化带来的好处相对较小。
