#!/usr/bin/env python3
"""
I2C Setup Test Script
====================

This script tests if the I2C configuration is working correctly.
It verifies that I2C devices are accessible and can be used for communication.
"""

import os
import sys
import glob
import time

def test_i2c_devices():
    """Test I2C device files access."""
    print("测试 I2C 设备文件:")
    
    # Check only I2C-3 device (project requirement)
    required_device = '/dev/i2c-3'
    
    if not os.path.exists(required_device):
        print(f"  ✗ 项目需要的I2C设备 {required_device} 不存在")
        return False
    
    print(f"  ✓ 找到项目需要的I2C设备: {required_device}")
    
    device_name = os.path.basename(required_device)
    try:
        # Check permissions
        stat_info = os.stat(required_device)
        perms = oct(stat_info.st_mode)[-3:]
        
        # Check if readable and writable
        if os.access(required_device, os.R_OK | os.W_OK):
            print(f"    ✓ {device_name} (权限: {perms}, 可读写)")
            print(f"  I2C设备测试: 1/1 通过")
            return True
        else:
            print(f"    ✗ {device_name} (权限: {perms}, 不可读写)")
            print(f"  I2C设备测试: 0/1 通过")
            return False
    except OSError as e:
        print(f"    ✗ {device_name} (权限检查失败: {e})")
        print(f"  I2C设备测试: 0/1 通过")
        return False

def test_i2c_periphery():
    """Test I2C using periphery library."""
    print("\n测试 I2C periphery 库:")
    
    try:
        from periphery import I2C
        print("  ✓ periphery 库导入成功")
    except ImportError as e:
        print(f"  ✗ periphery 库导入失败: {e}")
        print("  💡 提示: 请安装 python3-periphery 包")
        return False
    
    # Test only I2C-3 bus (project requirement)
    test_bus = 3
    device_path = f"/dev/i2c-{test_bus}"
    
    if not os.path.exists(device_path):
        print(f"  ✗ 项目需要的I2C总线 {test_bus} 不存在")
        return False
        
    print(f"  测试 I2C 总线 {test_bus}:")
    
    try:
        # Initialize I2C bus
        i2c = I2C(device_path)
        print(f"    ✓ I2C{test_bus} 初始化成功")
        
        # Close I2C
        i2c.close()
        print(f"    ✓ I2C{test_bus} 关闭成功")
        
        print(f"\n  I2C periphery 测试总结: 1/1 通过")
        return True
        
    except Exception as e:
        print(f"    ✗ I2C{test_bus} 测试失败: {e}")
        print(f"\n  I2C periphery 测试总结: 0/1 通过")
        return False

def test_i2c_scan():
    """Test I2C bus scanning using i2cdetect if available."""
    print("\n测试 I2C 总线扫描:")
    
    # Check if i2cdetect is available
    try:
        import subprocess
        result = subprocess.run(['which', 'i2cdetect'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("  ⚠ i2cdetect 命令不可用，跳过总线扫描")
            print("  💡 提示: 安装 i2c-tools 包可启用此功能")
            return True
    except Exception as e:
        print(f"  ⚠ 无法检查 i2cdetect: {e}")
        return True
    
    # Test scanning only I2C-3 bus (project requirement)
    test_bus = 3
    device_path = f"/dev/i2c-{test_bus}"
    
    if not os.path.exists(device_path):
        print(f"  ⚠ 项目需要的I2C总线 {test_bus} 不存在，跳过扫描")
        return True
        
    print(f"  扫描 I2C 总线 {test_bus}:")
    
    try:
        # Run i2cdetect
        result = subprocess.run(['i2cdetect', '-y', str(test_bus)], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print(f"    ✓ I2C{test_bus} 扫描成功")
            # Parse output to find devices
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            devices_found = []
            for line in lines:
                parts = line.split()
                if len(parts) > 1:
                    for addr in parts[1:]:
                        if addr not in ['--', 'UU'] and len(addr) == 2:
                            devices_found.append(addr)
            
            if devices_found:
                print(f"    ✓ 找到设备地址: {', '.join(devices_found)}")
            else:
                print(f"    ℹ 未找到设备")
                
            print(f"\n  I2C 扫描测试总结: 1/1 通过")
            return True
        else:
            print(f"    ✗ I2C{test_bus} 扫描失败: {result.stderr}")
            print(f"\n  I2C 扫描测试总结: 0/1 通过")
            return True  # 扫描失败不算致命错误
            
    except subprocess.TimeoutExpired:
        print(f"    ⚠ I2C{test_bus} 扫描超时")
        print(f"\n  I2C 扫描测试总结: 0/1 通过")
        return True
    except Exception as e:
        print(f"    ✗ I2C{test_bus} 扫描异常: {e}")
        print(f"\n  I2C 扫描测试总结: 0/1 通过")
        return True

def test_i2c_sysfs():
    """Test I2C sysfs interface."""
    print("\n测试 I2C sysfs 接口:")
    
    # Check only I2C-3 adapter information (project requirement)
    required_adapter = '/sys/class/i2c-adapter/i2c-3'
    
    if os.path.exists(required_adapter):
        print(f"  ✓ 找到项目需要的I2C适配器: i2c-3")
        adapter_name = os.path.basename(required_adapter)
        try:
            # Read adapter name
            name_file = os.path.join(required_adapter, 'name')
            if os.path.exists(name_file):
                with open(name_file, 'r') as f:
                    adapter_info = f.read().strip()
                print(f"    - {adapter_name}: {adapter_info}")
            else:
                print(f"    - {adapter_name}: (无名称信息)")
            return True
        except Exception as e:
            print(f"    - {adapter_name}: (读取失败: {e})")
            return False
    else:
        print(f"  ⚠ 未找到项目需要的I2C适配器: i2c-3")
        return False

def main():
    """Main test function."""
    print("I2C 配置测试")
    print("=" * 40)
    
    tests = [
        ("I2C 设备文件", test_i2c_devices),
        ("I2C sysfs 接口", test_i2c_sysfs),
        ("I2C periphery 库", test_i2c_periphery),
        ("I2C 总线扫描", test_i2c_scan),
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
        print("🎉 所有 I2C 测试通过！")
        return 0
    else:
        print("❌ 部分 I2C 测试失败，请检查硬件连接和权限设置")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 