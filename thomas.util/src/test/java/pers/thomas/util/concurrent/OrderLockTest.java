package pers.thomas.util.concurrent;

import java.io.IOException;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.junit.Test;

public class OrderLockTest {
	
	volatile static long valueTotal=0;

	@Test
	public void testLock() throws IOException {

		
		long startTime=System.currentTimeMillis();
		ExecutorService es=Executors.newFixedThreadPool(10);
		
		long total=10000000;
		CountDownLatch countdown=new CountDownLatch((int) total);
		StringBuilder sb=new StringBuilder();
		
		for(long i=0;i<total;i++){
			es.submit(new Task(String.valueOf(((long)(Math.random()*100000d))), String.valueOf(i), countdown,sb));
		}
		
		try {
			countdown.await();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		long endTime=System.currentTimeMillis();
		System.out.println(((double)(endTime-startTime))/((double)(total)));
		System.out.println(valueTotal);
		
		es.shutdown();
	}
	
	public static class Task implements Runnable{
		private String key;
		private String value;
		private CountDownLatch countdown;
		private StringBuilder sb;
		
		public Task(String key,String value,CountDownLatch countdown,StringBuilder sb ){
			this.key=key;
			this.value=value;
			this.countdown=countdown;
			this.sb=sb;
		}

		public void run() {
			
			try{
				OrderLock.lock(key);
				valueTotal=valueTotal+1;				
			}
			finally{
				OrderLock.unlock(key);				
			}
			countdown.countDown();			
		}
		
	}

}
