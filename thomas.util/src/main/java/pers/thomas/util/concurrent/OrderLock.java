package pers.thomas.util.concurrent;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;


/***
 * 
 * @author zhuxiang
 *
 * This class is designed to make access to a object (key) serialize.
 * 
 *  E.g. if want to make all the provision request to one user is processed one by one, the user's identifier can use as the lock key.
 *  
 *  Usage:
 *  try{
 *  	OrderLock.lock(key);
 *  	<Your Code>
 *  }finally{
 *  	unlock(key);
 *  }
 */
public class OrderLock {	
	private static ConcurrentHashMap<String,LockGroup> lockMap=new ConcurrentHashMap<String,LockGroup>();
	
	public static void lock(String key){
		while(true){
			LockGroup lockGroup=lockMap.get(key);			
			if(lockGroup!=null){
				lockGroup.getOperationLock().lock();
				if(lockMap.get(key)==lockGroup){
					break;
				}else{
					lockGroup.getOperationLock().unlock();
				}
			}else{
				lockGroup=new LockGroup();
				lockGroup.getQueueSize().incrementAndGet();
				lockGroup.getOperationLock().lock();
				lockMap.putIfAbsent(key, lockGroup);
				if(lockMap.get(key)==lockGroup){
					break;					
				}else{
					lockGroup.getOperationLock().unlock();
				}	
			}
		}		
	}
	
	public static void unlock(String key){		
		LockGroup lockGroup=lockMap.get(key);
		long size=lockGroup.getQueueSize().decrementAndGet();
		if(size==0){
			lockMap.remove(key);
		}
		lockGroup.getOperationLock().unlock();		
	}
	
	public static class LockGroup{
		private ReentrantLock operationLock=new ReentrantLock(true);
		private AtomicLong queueSize=new AtomicLong();
		public ReentrantLock getOperationLock() {
			return operationLock;
		}
		public void setOperationLock(ReentrantLock operationLock) {
			this.operationLock = operationLock;
		}
		public AtomicLong getQueueSize() {
			return queueSize;
		}
		public void setQueueSize(AtomicLong queueSize) {
			this.queueSize = queueSize;
		}
	}	
}
