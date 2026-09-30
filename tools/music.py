import numpy as np, wave
SR=44100
def tone(f,dur,amp=0.3,decay=4.0):
    t=np.arange(int(SR*dur))/SR
    w=np.sin(2*np.pi*f*t)+0.35*np.sin(2*np.pi*2*f*t)+0.12*np.sin(2*np.pi*3.01*f*t)
    env=np.exp(-decay*t)*np.minimum(1,t*200)
    return amp*w*env
def track(seconds, path, seed=0, bpm=112):
    rng=np.random.default_rng(seed); beat=60/bpm; n=int(SR*(seconds+1)); out=np.zeros(n)
    scale=[220.0,261.63,293.66,329.63,392.0,440.0,523.25,587.33,659.26]  # A minor pentatonic
    bass=[110.0,87.31,98.0,82.41]  # A F G E
    phrase=[rng.integers(2,9) for _ in range(8)]
    step=beat/2; i=0; t=0.0
    while t<seconds:
        bar=int(t/(beat*4))%4
        if i%8==0:  # bass each bar half
            s=int(t*SR); b=tone(bass[bar],beat*2,0.22,2.5); out[s:s+len(b)]+=b[:n-s]
        if i%16 in (0,3,6,8,11,14) or rng.random()<0.25:
            idx=phrase[(i//2)%8] if rng.random()<0.8 else rng.integers(2,9)
            s=int(t*SR); m=tone(scale[idx]*2,step*3,0.16,5.0); out[s:s+len(m)]+=m[:n-s]
        if i%4==2:  # soft tick
            s=int(t*SR); k=np.random.default_rng(i).normal(0,1,int(SR*0.03))*np.exp(-np.arange(int(SR*0.03))/300)*0.03; out[s:s+len(k)]+=k[:n-s]
        i+=1; t+=step
    out=out[:int(SR*seconds)]
    fade=int(SR*1.2); out[-fade:]*=np.linspace(1,0,fade); out[:2000]*=np.linspace(0,1,2000)
    out/=max(1e-6,np.abs(out).max())/0.7
    pcm=(out*32767).astype(np.int16); st=np.stack([pcm,pcm],1)
    with wave.open(path,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
