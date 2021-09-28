package kz.edu.nu.cs.se;

public class IdleState extends State {

    public IdleState(VendingMachine vm){
        this.vendingMachine = vm;
        this.name = "IdleState";
    }

    @Override
    public void insertCoin(int coin){
        if(coin != 50 && coin !=100){
            throw new IllegalArgumentException("Put another coin");
        } else {
            this.vendingMachine.setCurrentState(vendingMachine.enteringCoins);
            this.vendingMachine.balance += coin;
        }
    }

    @Override
    public int refund(){
        int compensation = this.vendingMachine.balance;
        this.vendingMachine.balance = 0;
        this.vendingMachine.setCurrentState(vendingMachine.idle);
        return compensation;
    }

    @Override
    public int vend(){
        if(this.vendingMachine.balance >= 200){
            this.vendingMachine.balance -= 200;
            return this.vendingMachine.refund();
        } else {
            throw new IllegalStateException("Add more money");
        }
    }

}
