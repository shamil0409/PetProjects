package kz.edu.nu.cs.se;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import org.junit.Before;
import org.junit.Test;

public class VendingMachineStatePatternTest {
    VendingMachine vm;
    
    @Before
    public void setUp() {
        this.vm = new VendingMachine();
    }
    
    @Test
    public void test_1() {
        assertTrue("In idle state after instantiation", vm.getCurrentState().equals(vm.idle));
    }
    
    @Test
    public void test_2() {
        vm.insertCoin(50);
        vm.insertCoin(100);

        assertTrue("Balance after adding 50 then 100 is 150", vm.getBalance() == 150);
        assertTrue("In entering coins state", vm.getCurrentState().equals(vm.enteringCoins));
    }
    
    @Test
    public void test_3() {
        vm.insertCoin(100);
        vm.insertCoin(100);

        assertTrue("Balance after 100,100 is 200", vm.getBalance() == 200);
        assertTrue("In paid state", this.vm.getCurrentState().equals(this.vm.paid));
    }
    
    @Test
    public void test_4() {
        try {
            vm.vend();
            fail("Expected Exception");
        } catch (IllegalStateException e) {
            assertTrue(true);
        } catch (Exception e) {
            fail("Expected Illegal State Exception");
        }
    }
    
    @Test
    public void test_5() {
        try {
            vm.insertCoin(60);
            fail("Expected Exception");
        } catch (IllegalArgumentException e) {
            assertTrue(true);
        } catch (Exception e) {
            fail("Expected Illegal Argument Exception");
        }
    }
    
    @Test
    public void test_6() {
        vm.insertCoin(50);
        vm.insertCoin(100);
        vm.insertCoin(100);
        vm.insertCoin(50);
        
        assertTrue("Paid Extra Balance is 300", vm.getBalance() == 300);
        
        int refundedAmount = vm.vend();
        
        assertTrue("Refunded 100", refundedAmount == 100);
        assertTrue("In Idle State", vm.getCurrentState().equals(vm.idle));
    }
    
    @Test
    public void test_7() {
        vm.insertCoin(50);
        vm.refund();
        vm.insertCoin(100);
        
        assertTrue("In Entering Coins State", vm.getCurrentState().equals(vm.enteringCoins));
        
        vm.insertCoin(100);
        vm.insertCoin(50);
        
        int refundedAmount = vm.refund();
        
        assertTrue("Refunded 100", refundedAmount == 250);
        assertTrue("Balance", vm.getBalance() == 0);
    }
    
    @Test
    public void test_8() {
        vm.insertCoin(50);
        
        try {
            vm.vend();
            fail("Expected Exception");
        } catch (IllegalStateException e) {
            assertTrue(true);
        } catch (Exception e) {
            fail("Expected Illegal State Exception");
        }
    }
    
    @Test
    public void test_9() {
        int refundedAmount = vm.refund();
        
        assertTrue("Refund in Idle", refundedAmount == 0);
    }
}
