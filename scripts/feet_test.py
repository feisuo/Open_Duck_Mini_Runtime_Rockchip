from mini_bdx_runtime.feet_contacts import FeetContacts
import time
import sys

class FeetTester:
    def __init__(self):
        self.detector = FeetContacts()
        self.running = False
        
    def format_status(self, status):
        """格式化状态输出"""
        return ("[接触]" if status[0] else "[悬空]", 
                "[接触]" if status[1] else "[悬空]")
    
    def run(self, interval=0.5):
        """主测试循环"""
        self.running = True
        print("脚部接触检测启动 (Ctrl+C退出)")
        print("-" * 40)
        
        try:
            while self.running:
                status = self.detector.get()
                left, right = self.format_status(status)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                
                print(f"{timestamp} 左脚{left} 右脚{right}")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n检测正常终止")
        except Exception as e:
            print(f"\n检测异常: {str(e)}", file=sys.stderr)
            return 1
        return 0

if __name__ == "__main__":
    tester = FeetTester()
    sys.exit(tester.run())
