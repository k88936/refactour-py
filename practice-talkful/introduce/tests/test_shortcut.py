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
        print(event.name)
    
    register_shortcut(Shortcut.F1, shortcut_handler)
    unregister_shortcut(Shortcut.F2)
    
    eventloop()


def shortcut_demo_all_keys(conn):
    from shortcut.api import register_shortcut
    from shortcut.types import ShortcutEvent, Shortcut
    from eventloop import eventloop

    redirect_stdio_to(conn)
    
    def shortcut_handler(event: ShortcutEvent):
        print(f"F{event.name}")
    
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
        self.parent_conn.send("shortcut F1 PRESSED\n")
        output = collect_output(self.parent_conn)
        self.assertIn("PRESSED", output)
    
    def test_f1_released_event(self):
        """Test F1 with RELEASED event"""
        self.parent_conn.send("shortcut F1 RELEASED\n")  # F1 RELEASED
        output = collect_output(self.parent_conn)
        self.assertIn("RELEASED", output)
    
    def test_f2_unregistered(self):
        """Test that F2 (unregistered) is ignored"""
        self.parent_conn.send("shortcut F2 PRESSED\n")  # F2 PRESSED
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
    
    def test_f5_pressed(self):
        """Test F5 PRESSED"""
        self.parent_conn.send("shortcut F5 PRESSED\n")
        output = collect_output(self.parent_conn)
        self.assertIn("PRESSED", output)
    
    def test_f8_released(self):
        """Test F8 RELEASED"""
        self.parent_conn.send("shortcut F8 RELEASED\n")
        output = collect_output(self.parent_conn)
        self.assertIn("RELEASED", output)


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
        self.parent_conn.send("shortcut INVALID 1\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_invalid_event_id(self):
        """Test invalid event ID"""
        self.parent_conn.send("shortcut F1 INVALID\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_missing_event_id(self):
        """Test event with missing event ID"""
        self.parent_conn.send("shortcut F1\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_negative_shortcut_id(self):
        """Test negative shortcut ID"""
        self.parent_conn.send("shortcut NEG_F1 1\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_negative_event_id(self):
        """Test negative event ID"""
        self.parent_conn.send("shortcut F1 NEG_PRESSED\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_non_numeric_shortcut_id(self):
        """Test non-numeric shortcut ID"""
        self.parent_conn.send("shortcut unknown_key 1\n")
        time.sleep(0.3)
        self.p.join(timeout=1)
        self.assertFalse(self.p.is_alive())
    
    def test_non_numeric_event_id(self):
        """Test non-numeric event ID"""
        self.parent_conn.send("shortcut F1 unknown_event\n")
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
        self.parent_conn.send("shortcut F1 PRESSED\n")  # F1 PRESSED
        output = collect_output(self.parent_conn)
        self.assertIn("PRESSED", output)
    
    def test_sequence_different_keys(self):
        """Test sequence of different keys with EOF after each"""
        # First key
        self.parent_conn.send("shortcut F1 PRESSED\n")  # F1 PRESSED
        output1 = collect_output(self.parent_conn)
        self.assertIn("PRESSED", output1)
        
        # Restart process for next event
        self.p.terminate()
        self.p.join(timeout=1)
        
        # Start new process
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.p = multiprocessing.Process(target=shortcut_demo_all_keys, args=(self.child_conn,))
        self.p.start()
        
        # Second key
        self.parent_conn.send("shortcut F4 PRESSED\n")  # F4 PRESSED
        output2 = collect_output(self.parent_conn)
        self.assertIn("PRESSED", output2)

if __name__ == '__main__':
    unittest.main()