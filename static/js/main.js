const tl = gsap.timeline();

tl.from(".hero-text", {
    opacity: 0,
    y: 200,
    duration: 1,
    ease: "power2.out"
}, 0.5); 

tl.from(".hero-img-1", {
    y: 200,
    opacity: 0,
    duration: 1,
    ease: "power2.out"
}, 1.5);

tl.from(".hero-img-2", {
    y: -500,
    opacity: 0,
    duration: 1,
    ease: "power2.out"
}, 2.5);

tl.from(".hero-img-3", {
    y: 400,
    opacity: 0,
    duration: 1,
    ease: "power2.out"
}, 3.5);

gsap.from(".card1", {
    opacity:0,
    x : -1200,
    y : 200,
    ease: "power3.out",
    scrollTrigger:{
        trigger:".card1",
        scroller :"body", 
        // markers: true,
        start: "top 70%",
        end: "top 50%",
        // scrub:3,
        // pin:true
    }
})

gsap.from(".card2", {
    opacity:0,
    x : 1200,
    y : 200,
    ease: "power3.out",
    scrollTrigger:{
        trigger:".card2",
        scroller :"body", 
        // markers: true,
        start: "top 70%",
        end: "top 50%",
        // scrub:3,
        // pin:true
    }
})

gsap.from("#red", {
    opacity:0,
    scale : 0.4,
    ease: "power2.out",
    
    scrollTrigger:{
        trigger:"#red",
        scroller :"body", 
        // markers: true,
        start: "top 80%",
        end: "top 30%",
        scrub:3,
        // pin:true
        // stagger: 0.1,
        
    }

})