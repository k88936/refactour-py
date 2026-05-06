import multiprocessing
import unittest
import time
from tests.utils import redirect_stdio_to, collect_output


def shortcut_demo(conn):
    redirect_stdio_to(conn)

    from shortcut.api import register_shortcut, unregister_shortcut
    from shortcut.types import ShortcutEvent, Shortcut
    from eventloop import eventloop

    def shortcut_handler(event: ShortcutEvent):
        print(event)
    
    register_shortcut(Shortcut.F1, shortcut_handler)
    unregister_shortcut(Shortcut.F2)
    
    eventloop()


def shortcut_demo_all_keys(conn):
    from shortcut.api import register_shortcut
    from shortcut.types import ShortcutEvent, Shortcut
    from eventloop import eventloop

    redirect_stdio_to(conn)
    
    def shortcut_handler(event: ShortcutEvent):
        print(f"F{event.value}")
    
    for shortcut in Shortcut:
        register_shortcut(shortcut, shortcut_handler)
    
    eventloop()


class ShortcutTest(unittest.TestCase):

    def setUp(self):
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target=shortcut_demo, args=(self.child_conn,))
        self.p.start()
    
    def tearDown(self):
        self.parent_conn.close()
        self.p.terminate()

    def test_register_and_trigger(self):
        """Test registering F1 and triggering PRESSED event"""
        self.parent_conn.send("shortcut 0 1\n")
        output = collect_output(self.parent_conn)
        self.assertIn("1", output)
    
    def test_f1_released_event(self):
        """Test F1 with RELEASED event"""
        self.parent_conn.send("shortcut 0 2\n")  # F1 RELEASED
        output = collect_output(self.parent_conn)
        self.assertIn("2", output)
    
    def test_f2_unregistered(self):
        """Test that F2 (unregistered) is ignored"""
        self.parent_conn.send("shortcut 1 1\n")  # F2 PRESSED
        output = collect_output(self.parent_conn)
        self.assertEqual(output,"")



class ShortcutAllKeysTest(unittest.TestCase):
    """Test all shortcut keys F1-F8"""
    
    def setUp(self):
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target=shortcut_demo_all_keys, args=(self.child_conn,))
        self.p.start()
    
    def tearDown(self):
        self.parent_conn.close()
        self.p.terminate()
    
    def test_f1_pressed(self):
        """Test F1 (id=0) PRESSED"""
        self.parent_conn.send("shortcut 0 1\n")
        output = collect_output(self.parent_conn)
        self.assertIn("1", output)
    
    def test_f3_released(self):
        """Test F3 (id=2) RELEASED"""
        self.parent_conn.send("shortcut 2 2\n")
        output = collect_output(self.parent_conn)
        self.assertIn("2", output)
    
    def test_f5_pressed(self):
        """Test F5 (id=4) PRESSED"""
        self.parent_conn.send("shortcut 4 1\n")
        output = collect_output(self.parent_conn)
        self.assertIn("1", output)
    
    def test_f8_released(self):
        """Test F8 (id=7, last key) RELEASED"""
        self.parent_conn.send("shortcut 7 2\n")
        output = collect_output(self.parent_conn)
        self.assertIn("2", output)


class ShortcutErrorHandlingTest(unittest.TestCase):
    """Test error handling for invalid inputs"""
    
    def setUp(self):
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target=shortcut_demo_all_keys, args=(self.child_conn,))
        self.p.start()
    
    def tearDown(self):
        self.parent_conn.close()
        self.p.terminate()
    
    def test_invalid_shortcut_id(self):
        """Test invalid shortcut ID (out of range)"""
        self.parent_conn.send("shortcut 99 1\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_invalid_event_id(self):
        """Test invalid event ID"""
        self.parent_conn.send("shortcut 0 99\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_missing_event_id(self):
        """Test event with missing event ID"""
        self.parent_conn.send("shortcut 0\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_negative_shortcut_id(self):
        """Test negative shortcut ID"""
        self.parent_conn.send("shortcut -1 1\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_negative_event_id(self):
        """Test negative event ID"""
        self.parent_conn.send("shortcut 0 -1\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_non_numeric_shortcut_id(self):
        """Test non-numeric shortcut ID"""
        self.parent_conn.send("shortcut abc 1\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_non_numeric_event_id(self):
        """Test non-numeric event ID"""
        self.parent_conn.send("shortcut 0 xyz\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())


class ShortcutSequentialTest(unittest.TestCase):
    """Test sequential events"""
    
    def setUp(self):
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target=shortcut_demo_all_keys, args=(self.child_conn,))
        self.p.start()
    
    def tearDown(self):
        if self.parent_conn:
            self.parent_conn.close()
        if self.p.is_alive():
            self.p.terminate()
            self.p.join(timeout=1)
            if self.p.is_alive():
                self.p.kill()
    
    def test_single_key(self):
        """Test single key press"""
        self.parent_conn.send("shortcut 0 1\n")  # F1 PRESSED
        output = collect_output(self.parent_conn)
        self.assertIn("1", output)
    
    def test_sequence_different_keys(self):
        """Test sequence of different keys with EOF after each"""
        # First key
        self.parent_conn.send("shortcut 0 1\n")  # F1 PRESSED
        output1 = collect_output(self.parent_conn)
        self.assertIn("1", output1)
        
        # Restart process for next event
        self.p.terminate()
        self.p.join(timeout=1)
        
        # Start new process
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target=shortcut_demo_all_keys, args=(self.child_conn,))
        self.p.start()
        
        # Second key
        self.parent_conn.send("shortcut 3 1\n")  # F4 PRESSED
        output2 = collect_output(self.parent_conn)
        self.assertIn("1", output2)

if __name__ == '__main__':
    unittest.main()