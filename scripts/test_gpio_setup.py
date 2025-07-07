#!/usr/bin/env python3
"""
GPIO Setup Test Script
======================

This script tests if the GPIO configuration is working correctly.
It verifies that GPIO devices are accessible and can be controlled.
"""

import os
import sys
import glob
import time

def test_gpio_sysfs():
    """Test GPIO sysfs interface access."""
    print("测试 GPIO sysfs 接口:")
    
    # Check if GPIO export/unexport files exist and are accessible
    gpio_export = '/sys/class/gpio/export'
    gpio_unexport = '/sys/class/gpio/unexport'
    
    if os.path.exists(gpio_export):
        if os.access(gpio_export, os.W_OK):
            print("  ✓ GPIO export 文件可写")
        else:
            print("  ✗ GPIO export 文件不可写")
            return False
    else:
        print("  ✗ GPIO export 文件不存在")
        return False
    
    if os.path.exists(gpio_unexport):
        if os.access(gpio_unexport, os.W_OK):
            print("  ✓ GPIO unexport 文件可写")
        else:
            print("  ✗ GPIO unexport 文件不可写")
            return False
    else:
        print("  ✗ GPIO unexport 文件不存在")
        return False
    
    # Check GPIO chips
    gpio_chips = glob.glob('/sys/class/gpio/gpiochip*')
    if gpio_chips:
        print(f"  ✓ 找到 {len(gpio_chips)} 个 GPIO 芯片:")
        for chip in gpio_chips:
            chip_name = os.path.basename(chip)
            print(f"    - {chip_name}")
    else:
        print("  ⚠ 未找到 GPIO 芯片")
    
    return True

def test_gpio_periphery():
    """Test GPIO using periphery library."""
    print("\n测试 GPIO periphery 库:")
    
    try:
        from periphery import GPIO
        print("  ✓ periphery 库导入成功")
    except ImportError as e:
        print(f"  ✗ periphery 库导入失败: {e}")
        return False
    
    # Test GPIO pins used in the project
    test_pins = [
        {'pin': 133, 'name': 'LEFT_EYE_GPIO', 'direction': 'out'},
        {'pin': 119, 'name': 'RIGHT_EYE_GPIO', 'direction': 'out'},
        {'pin': 125, 'name': 'PROJECTOR_GPIO', 'direction': 'out'},
        {'pin': 124, 'name': 'INPUT_GPIO_1', 'direction': 'in'},
        {'pin': 138, 'name': 'INPUT_GPIO_2', 'direction': 'in'},
    ]
    
    success_count = 0
    
    for pin_info in test_pins:
        pin_num = pin_info['pin']
        pin_name = pin_info['name']
        direction = pin_info['direction']
        
        try:
            print(f"  测试 GPIO {pin_num} ({pin_name}):")
            
            # Initialize GPIO
            gpio = GPIO(pin_num, direction)
            print(f"    ✓ GPIO {pin_num} 初始化成功")
            
            if direction == 'out':
                # Test write operations
                gpio.write(True)
                print(f"    ✓ GPIO {pin_num} 写入高电平成功")
                time.sleep(0.1)
                
                gpio.write(False)
                print(f"    ✓ GPIO {pin_num} 写入低电平成功")
                time.sleep(0.1)
            elif direction == 'in':
                # Test read operations
                value = gpio.read()
                print(f"    ✓ GPIO {pin_num} 读取成功，当前值: {value}")
                time.sleep(0.1)
            
            # Close GPIO
            gpio.close()
            print(f"    ✓ GPIO {pin_num} 关闭成功")
            
            success_count += 1
            
        except Exception as e:
            print(f"    ✗ GPIO {pin_num} 测试失败: {e}")
    
    print(f"\n  GPIO 测试总结: {success_count}/{len(test_pins)} 通过")
    
    return success_count == len(test_pins)

def test_gpio_devices():
    """Test GPIO device files."""
    print("\n测试 GPIO 设备文件:")
    
    # Check /dev/gpiochip* devices
    gpio_devices = glob.glob('/dev/gpiochip*')
    if gpio_devices:
        print(f"  ✓ 找到 {len(gpio_devices)} 个 GPIO 设备:")
        for device in gpio_devices:
            device_name = os.path.basename(device)
            try:
                stat_info = os.stat(device)
                perms = oct(stat_info.st_mode)[-3:]
                print(f"    - {device_name} (权限: {perms})")
            except OSError as e:
                print(f"    - {device_name} (无法读取权限: {e})")
    else:
        print("  ⚠ 未找到 GPIO 设备文件")
    
    # Check /dev/gpiomem
    if os.path.exists('/dev/gpiomem'):
        try:
            stat_info = os.stat('/dev/gpiomem')
            perms = oct(stat_info.st_mode)[-3:]
            print(f"  ✓ /dev/gpiomem 存在 (权限: {perms})")
        except OSError as e:
            print(f"  ✗ /dev/gpiomem 权限检查失败: {e}")
    else:
        print("  ⚠ /dev/gpiomem 不存在")
    
    return True

def main():
    """Main test function."""
    print("GPIO 配置测试")
    print("=" * 40)
    
    tests = [
        ("GPIO sysfs 接口", test_gpio_sysfs),
        ("GPIO 设备文件", test_gpio_devices),
        ("GPIO periphery 库", test_gpio_periphery),
    ]
    
    success_count = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"运行测试: {test_name}")
        print(f"{'='*50}")
        
        try:
            if test_func():
                print(f"✓ {test_name} 测试通过")
                success_count += 1
            else:
                print(f"✗ {test_name} 测试失败")
        except Exception as e:
            print(f"✗ {test_name} 测试异常: {e}")
    
    print(f"\n{'='*50}")
    print(f"测试总结: {success_count}/{len(tests)} 通过")
    print(f"{'='*50}")
    
    if success_count == len(tests):
        print("🎉 所有 GPIO 测试通过！")
        return 0
    else:
        print("❌ 部分 GPIO 测试失败，请检查硬件连接和权限设置")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 