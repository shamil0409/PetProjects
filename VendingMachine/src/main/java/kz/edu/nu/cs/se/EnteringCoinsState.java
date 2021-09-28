package kz.edu.nu.cs.se;

public class EnteringCoinsState extends State {
    public EnteringCoinsState(VendingMachine vm){
        this.vendingMachine = vm;
        this.name = "EnteringCoinState";
    }

    @Override
    public void insertCoin(int coin){
        if(coin != 50 && coin !=100){
            throw new IllegalArgumentException("Put another coin");
        } else {
            this.vendingMachine.balance += coin;
            if(this.vendingMachine.balance >= 200){
                this.vendingMachine.setCurrentState(vendingMachine.paid);
            }
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
