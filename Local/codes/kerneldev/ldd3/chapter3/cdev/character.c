#include <linux/init.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/slab.h>

#include "character.h"

MODULE_LICENSE("Dual BSD/GPL");


int scull_major =   SCULL_MAJOR;
int scull_minor =   0;
unsigned int scull_nr_devs = 1;
int scull_quantum = SCULL_QUANTUM;
int scull_qset =    SCULL_QSET;

struct scull_dev *scull_devices;	/* allocated in scull_init_module */


int scull_open(struct inode *inode, struct file *filp)
{
    printk("scull_open called");
    return 0;
}

int scull_release(struct inode *inode, struct file *filp)
{
    printk("scull_release called");
	return 0;
}

ssize_t scull_read(struct file *filp, char __user *buf, size_t count, loff_t *f_pos)
{
    ssize_t retval = 0;
    printk("scull_read called");

    return retval;
}


ssize_t scull_write(struct file *filp, const char __user *buf, size_t count,
                loff_t *f_pos)
{
    ssize_t retval = -ENOMEM;
    printk("scull_write called");

    return retval;
}

long scull_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
    int retval = 0;
    printk("scull_ioctl called");

    return retval;
}

loff_t scull_llseek(struct file *filp, loff_t off, int whence)
{
    loff_t newpos = 0;
    printk("scull_llseek called");
    return newpos;
}

struct file_operations scull_fops = {
    .owner = THIS_MODULE,
    .llseek =   scull_llseek,
    .read =     scull_read,
    .write =    scull_write,
    .unlocked_ioctl =    scull_ioctl,
    .open =     scull_open,
    .release =  scull_release,
};

static void scull_setup_cdev(struct scull_dev *dev, int index)
{
    int err;
    int devno = MKDEV(scull_major, scull_minor + index);
    
    cdev_init(&dev->cdev, &scull_fops);
    dev->cdev.owner = THIS_MODULE;
    dev->cdev.ops = &scull_fops;

    err = cdev_add(&dev->cdev, devno, 1);

    /* Fail gracefully if need be */
	if (err)
		printk(KERN_NOTICE "Error %d adding scull%d", err, index);
}

void scull_cleanup_module(void);

int scull_init_module(void)
{
    int results, i = 0;
    dev_t dev = 0;

    if (scull_major) {   
        dev = MKDEV(scull_major, scull_minor);
        results = register_chrdev_region(dev, scull_nr_devs, "scull");
    } else {
        results = alloc_chrdev_region(&dev, scull_minor,  scull_nr_devs, "scull");
        scull_major = MAJOR(dev);
    }

    if (results < 0) {
        printk(KERN_WARNING "scull: can't get major %d\n", scull_major);
        return results;
    }

    scull_devices = kmalloc(scull_nr_devs * sizeof(struct scull_dev), GFP_KERNEL);
    if (!scull_devices) {
		results = -ENOMEM;
		goto fail;  /* Make this more graceful */
	}
    
    for(; i < scull_nr_devs; i++) {
        scull_devices[i].quantum = scull_quantum;
        scull_devices[i].qset = scull_qset;
        mutex_init(&scull_devices[i].lock);
        scull_setup_cdev(&scull_devices[i], i);
    }

    return 0;

fail:
	scull_cleanup_module();
	return results;
}

void scull_cleanup_module(void)
{
    int i = 0;
    dev_t devno = MKDEV(scull_major, scull_minor);
    unregister_chrdev_region(devno, scull_nr_devs);
    
    /* Get rid of our char dev entries */
    if (scull_devices) {
        for (; i < scull_nr_devs; i++) {
            cdev_del(&scull_devices[i].cdev);
        }
        kfree(scull_devices);
    }
}

module_init(scull_init_module);
module_exit(scull_cleanup_module);
