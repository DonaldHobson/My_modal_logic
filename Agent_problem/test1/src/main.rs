//use std::mem;
use std::io::Write;
fn bits4(i:u16)->u64{
	let mut i=i.reverse_bits();
	let mut j=0u64;
	for _ in 0..16{
		j<<=4;
		j|=if (i&1)==1 {15}else{0};
		
		i>>=1;
	}
	j
}
fn calc(p1:u64,p2:u64)->u64{
	/*
	println!("{:#066b}",p2);
	let mut b=p2.to_ne_bytes();
	
	let s=b[1];
	b[1]=b[2];
	b[2]=s;
	
	let s=b[5];
	b[5]=b[6];
	b[6]=s;
	
	//mem::swap(&mut b[1],&mut b[2]);
	//mem::swap(&mut b[5], &mut b[6]);
	let p2=u64::from_ne_bytes(b);
	println!("{:#066b}\n",p2);
	let p1=p1^0x5555_5555_5555_5555;
	let p2=p2^0x3333_3333_3333_3333;*/
	let p3=p1&p2;
	let mut p=p3;
	//println!("{:#066b}",p);
	p|=p.wrapping_shl(32);
	p|=p.wrapping_shl(16);
	p|=p.wrapping_shl( 8);
	p|=p.wrapping_shl( 4);
	let p=p;
	//println!("{:#066b}",p);
	let mut k=p&15;
	//println!("k {:#06b}",k);
	k=(p>>(k*4))&15;
	//println!("k {:#06b}",k);
	k=(p>>(k*4))&15;
	//println!("k {:#06b}",k);
	k=(p>>(k*4))&15;
	//println!("k {:#06b}",k);
	let k2=(p>>(k*4))&15;
	//println!("{:#06b}",k);
	assert_eq!(k,k2);
	let d=(p3>>(k*4))&15;//1 2 4 8
	//println!("d {:#06b}",d);
	let d=(0x0000_0030_0020_1000u64 >>(d*4))&0x30;//0 16 32 48
	1<<d
}
fn spr(k:u64)->u64{
	let k=(0x0000_0030_0020_1000u64 >>(k*4))&0x30;
	1<<k
}





fn f4(c:u64,d:u64,k:u64)->u64{
	let k2=(c>>(15*4))&15;
	let k3=(d>>(15*4))&15;
	
		spr(k2)*(1<<11)+

		spr(k3)*(1<<11)
	
}


fn f3(c:u64,d:u64,k:u64)->u64{
	let k2=(c>>(k*4))&15;
	let k3=(d>>(k*4))&15;
	(if k|k2==k{
		spr(k2)*(1<<12)
	}else{
		f4(c,d,k|k2)
	})+(
	if k|k3==k{
		spr(k3)*(1<<12)
	}else{	
		f4(c,d,k|k3)
	})
}

fn f2(c:u64,d:u64,k:u64)->u64{
	let k2=(c>>(k*4))&15;
	let k3=(d>>(k*4))&15;
	(if k|k2==k{
		spr(k2)*(1<<13)
	}else{
		f3(c,d,k|k2)
	})+(
	if k|k3==k{
		spr(k3)*(1<<13)
	}else{	
		f3(c,d,k|k3)
	})
}
fn f1(c:u64,d:u64,k:u64)->u64{
	let k2=(c>>(k*4))&15;
	let k3=(d>>(k*4))&15;
	(if k|k2==k{
		spr(k2)*(1<<14)
	}else{
		f2(c,d,k|k2)
	})+(
	if k|k3==k{
		spr(k3)*(1<<14)
	}else{	
		f2(c,d,k|k3)
	})
}
fn lcalc(p:u64)->u64{
	let c=p&0x3333_3333_3333_3333;
	let d=p^c;
	//let mut k=c&15;
	f1(c,d,c&15)+f1(c,d,d&15)
	
	
}
fn main() {
	let mut vec=[0u64;1<<16];
	let mut cvec=[0u64;1<<16];
	let mut res=[0u64;1<<16];
	for i in 0..1<<16{
		let r=bits4(i as u16);
		
		vec[i]=r^0x5555_5555_5555_5555;
		
		let mut b=r.to_ne_bytes();
	
		let s=b[1];
		b[1]=b[2];
		b[2]=s;
		
		let s=b[5];
		b[5]=b[6];
		b[6]=s;
		
		cvec[i]=u64::from_ne_bytes(b)^0x3333_3333_3333_3333;
		
	}
	let vec=vec;
	let cvec=cvec;
	let fair=0xfff0usize;
	let coo=0x64usize;
	let def=0xffffusize;
	let timer = std::time::Instant::now();
	
	/*
	let block=512;
	let iblock=(1<<16)/block;
	let totb=(iblock*(iblock+1))/2;
	
	for ii in 0..iblock{
		
		for jj in 0..ii+1{
			for i in (ii*block)..(ii+1)*block{
				for j in (jj*block)..(jj+1)*block{
					let r=calc(vec[i],cvec[j]);
					res[i]+=r;
					if j<i {res[j]+=r;}
				}
			}
		}
		println!("{}%",(50*ii*(ii+1))/totb);
	}*/
	
	for i in 0..1<<16{
		res[i]=lcalc(vec[i]);//9.235435ms
	}
	println!("do_stuff: {:?}", timer.elapsed());//do_stuff: 18.706904588s
	println!("defect,  p2 wins, p1 wins, coop");
	println!("{:#066b}",calc(vec[coo],cvec[coo]));
	println!("{:#066b}",calc(vec[coo],cvec[def]));
	println!("{:#066b}",calc(vec[def],cvec[def]));
	println!("{:#066b}",calc(vec[coo],cvec[fair]));
	println!("df {:#066b}",calc(vec[def],cvec[fair]));
	println!("fd {:#066b}",calc(vec[fair],cvec[def]));
	println!("{:#066b}",calc(vec[fair],cvec[fair]));
	//println!("{:#066b}",vec[(1<<16)-1]);
	println!("Hello, world!{:?}",(1..5).collect::<Vec<_>>());
    println!("Hello, world!");
    
    

   let mut file = std::fs::File::create("data_file2").expect("create failed");
   file.write_all(&res.iter().map(|x| x.to_be_bytes()).collect::<Vec<_>>().concat()).expect("write failed");
   
   

   
}
