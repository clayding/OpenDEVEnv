## Using a device tree to describe a character driver

Add the contents in the following:

```
chrdev {
	compatible = "ldddc,chrdev";
	#address-cells = <1>;
	#size-cells = <0>;

	chrdev@2 {
		label = "cdev-eeprom";
		reg = <2>;
	};

	chrdev@4 {
		label = "cdev-rom";
		reg = <4>;
		read-only;
	};
};

root@KernelDev:~/linux# vi arch/arm/boot/dts/vexpress-v2p-ca9.dts
```

or apply the patch to arch/arm/boot/dts/vexpress-v2p-ca9.dts directly:
```
root@KernelDev:~/linux# patch -p1 < ~/workspace/kernel/docker4kernel/codes/ldddc/chapter4/chrdev/add_chrdev_devices.dts.patch
patching file arch/arm/boot/dts/vexpress-v2p-ca9.dts
```

Build dtb
root@KernelDev:~/linux# make dtbs


