#define pr_fmt(fmt) "%s:%s: " fmt, KBUILD_MODNAME, __func__
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/uaccess.h>

/* Device major umber */
static int major;

/* Device data */
#define BUF_LEN 300
static char chrdev_buf[BUF_LEN];

static ssize_t chrdev_read(struct file *filep,
                            char __user *buf, size_t count,
                            loff_t *ppos)
{
    int ret;
    pr_info("should read %ld bytes (*ppos=%lld)\n", count, *ppos);
    /* Check for end-of-buffer */
    if (*ppos + count >= BUF_LEN)
        count = BUF_LEN - *ppos;
    /* Return data to the user space */
    ret = copy_to_user(buf, chrdev_buf + *ppos, count);
    if (ret < 0)
        return -EFAULT;
    *ppos += count;
    pr_info("return %ld bytes (*ppos=%lld)\n", count, *ppos);
    return count;
}

static ssize_t chrdev_write(struct file *filp,
                            const char __user *buf, size_t count,
                            loff_t *ppos)
{
    int ret;
    pr_info("should write %ld bytes (*ppos=%lld)\n", count, *ppos);
    /* Check for end-of-buffer */
    if (*ppos + count >= BUF_LEN)
        count = BUF_LEN - *ppos;
    /* Get data from the user space */
    ret = copy_from_user(chrdev_buf + *ppos, buf, count);
    if (ret < 0)
        return -EFAULT;
    *ppos += count;
    pr_info("got %ld bytes (*ppos=%lld)\n", count, *ppos);
    return count;
}

static int chrdev_open(struct inode *inode, struct file *filp)
{
    pr_info("chrdev opened\n");
    return 0;
}
static int chrdev_release(struct inode *inode, struct file *filp)
{
    pr_info("chrdev released\n");
    return 0;
}

static struct file_operations chrdev_fops = {
    .owner = THIS_MODULE,
    .read = chrdev_read,
    .write = chrdev_write,
    .open = chrdev_open,
    .release = chrdev_release
};

static int __init chrdev_init(void)
{
    int ret;
    ret = register_chrdev(0, "chrdev", &chrdev_fops);
    if (ret < 0) {
        pr_err("unable to register char device! Error %d\n", ret);
        return ret;
    }
    major = ret;
    pr_info("got major %d\n", major);
    return 0;
}

static void __exit chrdev_exit(void)
{
    unregister_chrdev(major, "chrdev");
}
module_init(chrdev_init);
module_exit(chrdev_exit);