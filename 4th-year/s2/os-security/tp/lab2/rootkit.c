#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/uaccess.h> 

#define PROCFS_NAME "rootkit" 

static ssize_t procfile_read(struct file *file, char __user *buffer, size_t length, loff_t *offset)
{
    static const char msg[] = "Hello from the kernel!\n"; 
    size_t msg_len = sizeof(msg) - 1; 

    if (*offset >= msg_len)
        return 0;

    if (length < msg_len)
        return -EINVAL; 

    if (copy_to_user(buffer, msg, msg_len))
        return -EFAULT; 

    *offset += msg_len; 
    return msg_len; 
}

static const struct proc_ops proc_file_fops = {
    .proc_read = procfile_read,
};

static int __init rootkit_init(void)
{
    proc_create(PROCFS_NAME, 0644, NULL, &proc_file_fops);
    printk(KERN_INFO "Module loaded\n");
    return 0; 
}

static void __exit rootkit_exit(void)
{
    remove_proc_entry(PROCFS_NAME, NULL); 
    printk(KERN_INFO "Module unloaded\n"); 
}

MODULE_LICENSE("GPL");
module_init(rootkit_init);
module_exit(rootkit_exit);
