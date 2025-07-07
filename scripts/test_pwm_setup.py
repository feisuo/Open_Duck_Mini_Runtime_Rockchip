#!/usr/bin/env python3
"""
PWM Setup Test Script
====================

This script tests if the PWM configuration is working correctly.
It verifies that PWM channels are exported and accessible.
"""

import os
import sys
import glob
import time

def test_pwm_channel(chip, channel):
    """Test a specific PWM channel."""
    chip_path = f"/sys/class/pwm/{chip}"
    pwm_path = f"{chip_path}/pwm{channel}"
    
    print(f"\n测试 {chip} 通道 {channel}:")
    
    # Check if PWM chip exists
    if not os.path.exists(chip_path):
        print(f"  ✗ PWM芯片 {chip} 不存在")
        return False
    
    print(f"  ✓ PWM芯片 {chip} 存在")
    
    # Check if PWM channel is exported
    if not os.path.exists(pwm_path):
        print(f"  ✗ PWM通道 {channel} 未导出")
        return False
    
    print(f"  ✓ PWM通道 {channel} 已导出")
    
    # Check PWM control files
    control_files = ['period', 'duty_cycle', 'enable', 'polarity']
    for control_file in control_files:
        file_path = f"{pwm_path}/{control_file}"
        if os.path.exists(file_path):
            try:
                # Test read access
                with open(file_path, 'r') as f:
                    value = f.read().strip()
                print(f"  ✓ {control_file}: {value} (可读)")
                
                # Test write access (only test write without actually changing values)
                if os.access(file_path, os.W_OK):
                    print(f"  ✓ {control_file}: 可写")
                else:
                    print(f"  ✗ {control_file}: 不可写")
                    return False
                    
            except Exception as e:
                print(f"  ✗ {control_file}: 访问错误 - {e}")
                return False
        else:
            print(f"  ✗ {control_file}: 文件不存在")
            return False
    
    return True

def test_pwm_basic_operation(chip, channel):
    """Test basic PWM operations."""
    pwm_path = f"/sys/class/pwm/{chip}/pwm{channel}"
    
    print(f"\n测试 {chip} 通道 {channel} 基本操作:")
    
    try:
        # Set period (1ms = 1000000 ns)
        with open(f"{pwm_path}/period", 'w') as f:
            f.write("1000000")
        print("  ✓ 设置周期成功")
        
        # Set duty cycle (25% = 250000 ns)
        with open(f"{pwm_path}/duty_cycle", 'w') as f:
            f.write("250000")
        print("  ✓ 设置占空比成功")
        
        # Enable PWM
        with open(f"{pwm_path}/enable", 'w') as f:
            f.write("1")
        print("  ✓ 启用PWM成功")
        
        # Wait a bit
        time.sleep(0.5)
        
        # Disable PWM
        with open(f"{pwm_path}/enable", 'w') as f:
            f.write("0")
        print("  ✓ 禁用PWM成功")
        
        # Reset duty cycle
        with open(f"{pwm_path}/duty_cycle", 'w') as f:
            f.write("0")
        print("  ✓ 重置占空比成功")
        
        return True
        
    except Exception as e:
        print(f"  ✗ PWM操作失败: {e}")
        return False

def main():
    """Main test function."""
    print("PWM 配置测试")
    print("=" * 40)
    
    # Test configuration from the setup script
    pwm_configs = [
        {'chip': 'pwmchip2', 'channel': 0, 'description': 'PWM2 Channel 0 (Pin 31)'},
        {'chip': 'pwmchip3', 'channel': 0, 'description': 'PWM3 Channel 0 (Pin 34)'}
    ]
    
    success_count = 0
    total_count = len(pwm_configs)
    
    for config in pwm_configs:
        print(f"\n{'='*50}")
        print(f"测试 {config['description']}")
        print(f"{'='*50}")
        
        # Test basic access
        if test_pwm_channel(config['chip'], config['channel']):
            print(f"  ✓ 基本访问测试通过")
            
            # Test basic operations
            if test_pwm_basic_operation(config['chip'], config['channel']):
                print(f"  ✓ 基本操作测试通过")
                success_count += 1
            else:
                print(f"  ✗ 基本操作测试失败")
        else:
            print(f"  ✗ 基本访问测试失败")
    
    print(f"\n{'='*50}")
    print(f"测试总结: {success_count}/{total_count} 通过")
    print(f"{'='*50}")
    
    if success_count == total_count:
        print("🎉 所有PWM测试通过！")
        return 0
    else:
        print("❌ 部分PWM测试失败，请检查硬件连接和权限设置")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 