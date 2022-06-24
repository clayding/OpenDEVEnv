#include <linux/module.h>
#include <linux/init.h>
#include <linux/sched.h>
#include <linux/time.h>
#include <linux/delay.h>
#include <linux/workqueue.h>

static DECLARE_WAIT_QUEUE_HEAD(my_mq);
static int condition = 0;

/*declare a work queue*/
static struct work_struct wrk;

static void work_handler(struct work_struct *work)
{
    printk("Wait queue module handler %s\n", __FUNCTION__);
    msleep(5000);
    printk("Wake up the sleeping module\n");
    condition = 1;
    /*
    The condition is then only rechecked each time you call
    wake_up_interruptible in the wait queue. If the condition
    is true when wake_up_interruptible runs, a process in the
    wait queue will be awakened, and its state set to TASK_RUNNING
    */
    wake_up_interruptible(&my_mq);
}


static int __init my_init(void)
{
    printk("Wait queue example\n");

    INIT_WORK(&wrk, work_handler);
    schedule_work(&wrk);

    printk("Going to sleep %s\n", __FUNCTION__);
    /*
    wait_event_interruptible does not continuously poll,
    but simply evaluates the condition when it is called.
    If the condition is false, the process is put into a 
    TASK_INTERRUPTIBLE state and removed from the run queue.
    */
    wait_event_interruptible(my_mq, condition != 0);

    pr_info("worken up by the work job\n");

    return 0;
}

void my_exit(void)
{
    printk("wait queue example cleanup\n");
}

module_init(my_init);
module_exit(my_exit)
MODULE_AUTHOR("ClayDing<gdskclay@gmail.com>");
MODULE_LICENSE("GPL");
