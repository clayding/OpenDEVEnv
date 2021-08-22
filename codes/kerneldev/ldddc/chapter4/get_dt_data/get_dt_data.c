/*
 * Module to inspect device tree from the kernel
 */

#define pr_fmt(fmt) "%s: " fmt, KBUILD_MODNAME
#include <linux/moduleparam.h>
#include <linux/module.h>
#include <linux/of.h>

#define PATH_DEFAULT "/"
static char *path = PATH_DEFAULT;
module_param(path, charp, S_IRUSR | S_IWUSR);
MODULE_PARM_DESC(path, "a device tree pathname" \
                        "(default is \"" PATH_DEFAULT"\")");

static void print_property_u32(struct device_node *node, const char
*name)
{
    u32 val32;
    if (of_property_read_u32(node, name, &val32) == 0)
        pr_info(" \%s = %d\n", name, val32);
}

static void print_property_string(struct device_node *node, const
char *name)
{
    const char *str;
    if (of_property_read_string(node, name, &str) == 0)
        pr_info(" \%s = %s\n", name, str);
}

static void print_main_prop(struct device_node *node)
{
    pr_info("+ node = %s\n", node->full_name);
    print_property_u32(node, "#address-cells");
    print_property_u32(node, "#size-cells");
    print_property_u32(node, "reg");
    print_property_string(node, "name");
    print_property_string(node, "compatible");
    print_property_string(node, "status");
}

static int __init get_dt_data_init(void)
{
    struct device_node *node, *child;
    struct property *prop;

    pr_info("path = \"%s\"\n", path);

    /* Find node by its pathname */
    node = of_find_node_by_path(path);
    if (!node) {
        pr_err("failed to find device-tree node \"%s\"\n", path);
        return -ENODEV;
    }
    pr_info("device-tree node found !\n");

    pr_info("now getting main properties...\n");
    print_main_prop(node);

    pr_info("now move through all properties...\n");
    for_each_property_of_node(node, prop)
        pr_info("-> %s\n", prop->name);

    /* Move through node's children... */
    pr_info("Now move through children...\n");
    for_each_child_of_node(node, child)
        print_main_prop(child);

    /* Force module unloading... */
    return -EINVAL;
}

static void __exit get_dt_data_exit(void)
{
    /* nop */
}

module_init(get_dt_data_init);
module_exit(get_dt_data_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ClayDing");
MODULE_DESCRIPTION("Module to inspect device tree from the kernel");
MODULE_VERSION("0.1");

/*
/mnt/host_share # insmod get_dt_data.ko
get_dt_data: path = "/"
get_dt_data: device-tree node found !
get_dt_data: now getting main properties...
get_dt_data: + node = /
get_dt_data:  #address-cells = 1
get_dt_data:  #size-cells = 1
get_dt_data:  name =
get_dt_data:  compatible = arm,vexpress,v2p-ca9
get_dt_data: now move through all properties...
get_dt_data: -> model
get_dt_data: -> arm,hbi
get_dt_data: -> arm,vexpress,site
get_dt_data: -> compatible
get_dt_data: -> interrupt-parent
get_dt_data: -> #address-cells
get_dt_data: -> #size-cells
get_dt_data: -> name
get_dt_data: Now move through children...
get_dt_data: + node = /virtio_mmio@10013000
get_dt_data:  reg = 268513280
get_dt_data:  name = virtio_mmio
get_dt_data:  compatible = virtio,mmio
get_dt_data: + node = /virtio_mmio@10013200
get_dt_data:  reg = 268513792
get_dt_data:  name = virtio_mmio
get_dt_data:  compatible = virtio,mmio
get_dt_data: + node = /virtio_mmio@10013400
get_dt_data:  reg = 268514304
get_dt_data:  name = virtio_mmio
get_dt_data:  compatible = virtio,mmio
get_dt_data: + node = /virtio_mmio@10013600
get_dt_data:  reg = 268514816
get_dt_data:  name = virtio_mmio
get_dt_data:  compatible = virtio,mmio
get_dt_data: + node = /chosen
get_dt_data:  name = chosen
get_dt_data: + node = /aliases
get_dt_data:  name = aliases
get_dt_data: + node = /cpus
get_dt_data:  #address-cells = 1
get_dt_data:  #size-cells = 0
get_dt_data:  name = cpus
get_dt_data: + node = /memory@60000000
get_dt_data:  reg = 1610612736
get_dt_data:  name = memory
get_dt_data: + node = /clcd@10020000
get_dt_data:  reg = 268566528
get_dt_data:  name = clcd
get_dt_data:  compatible = arm,pl111
get_dt_data: + node = /memory-controller@100e0000
get_dt_data:  reg = 269352960
get_dt_data:  name = memory-controller
get_dt_data:  compatible = arm,pl341
get_dt_data: + node = /memory-controller@100e1000
get_dt_data:  reg = 269357056
get_dt_data:  name = memory-controller
get_dt_data:  compatible = arm,pl354
get_dt_data: + node = /timer@100e4000
get_dt_data:  reg = 269369344
get_dt_data:  name = timer
get_dt_data:  compatible = arm,sp804
get_dt_data:  status = disabled
get_dt_data: + node = /watchdog@100e5000
get_dt_data:  reg = 269373440
get_dt_data:  name = watchdog
get_dt_data:  compatible = arm,sp805
get_dt_data: + node = /scu@1e000000
get_dt_data:  reg = 503316480
get_dt_data:  name = scu
get_dt_data:  compatible = arm,cortex-a9-scu
get_dt_data: + node = /timer@1e000600
get_dt_data:  reg = 503318016
get_dt_data:  name = timer
get_dt_data:  compatible = arm,cortex-a9-twd-timer
get_dt_data: + node = /watchdog@1e000620
get_dt_data:  reg = 503318048
get_dt_data:  name = watchdog
get_dt_data:  compatible = arm,cortex-a9-twd-wdt
get_dt_data: + node = /interrupt-controller@1e001000
get_dt_data:  #address-cells = 0
get_dt_data:  reg = 503320576
get_dt_data:  name = interrupt-controller
get_dt_data:  compatible = arm,cortex-a9-gic
get_dt_data: + node = /cache-controller@1e00a000
get_dt_data:  reg = 503357440
get_dt_data:  name = cache-controller
get_dt_data:  compatible = arm,pl310-cache
get_dt_data: + node = /pmu
get_dt_data:  name = pmu
get_dt_data:  compatible = arm,cortex-a9-pmu
get_dt_data: + node = /dcc
get_dt_data:  name = dcc
get_dt_data:  compatible = arm,vexpress,config-bus
get_dt_data: + node = /smb
get_dt_data:  #address-cells = 2
get_dt_data:  #size-cells = 1
get_dt_data:  name = smb
get_dt_data:  compatible = simple-bus
insmod: can't insert 'get_dt_data.ko': invalid parameter
*/


/*
/mnt/host_share # insmod get_dt_data.ko path=/cpus
get_dt_data: path = "/cpus"
get_dt_data: device-tree node found !
get_dt_data: now getting main properties...
get_dt_data: + node = /cpus
get_dt_data:  #address-cells = 1
get_dt_data:  #size-cells = 0
get_dt_data:  name = cpus
get_dt_data: now move through all properties...
get_dt_data: -> #address-cells
get_dt_data: -> #size-cells
get_dt_data: -> name
get_dt_data: Now move through children...
get_dt_data: + node = /cpus/cpu@0
get_dt_data:  reg = 0
get_dt_data:  name = cpu
get_dt_data:  compatible = arm,cortex-a9
get_dt_data: + node = /cpus/cpu@1
get_dt_data:  reg = 1
get_dt_data:  name = cpu
get_dt_data:  compatible = arm,cortex-a9
get_dt_data: + node = /cpus/cpu@2
get_dt_data:  reg = 2
get_dt_data:  name = cpu
get_dt_data:  compatible = arm,cortex-a9
get_dt_data: + node = /cpus/cpu@3
get_dt_data:  reg = 3
get_dt_data:  name = cpu
get_dt_data:  compatible = arm,cortex-a9
insmod: can't insert 'get_dt_data.ko': invalid parameter
*/

/*
/mnt/host_share # insmod get_dt_data.ko path=/smb/motherboard/mcc/osc@1
get_dt_data: path = "/smb/motherboard/mcc/osc@1"
get_dt_data: device-tree node found !
get_dt_data: now getting main properties...
get_dt_data: + node = /smb/motherboard/mcc/osc@1
get_dt_data:  name = osc
get_dt_data:  compatible = arm,vexpress-osc
get_dt_data: now move through all properties...
get_dt_data: -> compatible
get_dt_data: -> arm,vexpress-sysreg,func
get_dt_data: -> freq-range
get_dt_data: -> #clock-cells
get_dt_data: -> clock-output-names
get_dt_data: -> linux,phandle
get_dt_data: -> phandle
get_dt_data: -> name
get_dt_data: Now move through children...
insmod: can't insert 'get_dt_data.ko': invalid parameter
*/