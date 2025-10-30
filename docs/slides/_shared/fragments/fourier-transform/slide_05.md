
## Epicycles

Now at the start, I said it splits things into sine waves. The thing is, the sine waves it creates are not just regular sine waves, but they’re 3D. You could call them "complex sinusoids". Or just "spirals".

<canvas id="complex-sinusoid" class="sketch" width=500 height=500></canvas>

If we take a look from the side, they look like sine waves. From front on, though, these look like circles.

<canvas id="complex-sinusoid-turn" class="sketch" width=500 height=500></canvas>

So far everything we’ve been doing has only required the regular 2D sine waves. When we do a Fourier transform on 2D waves, the complex parts cancel out so we just end up with sine waves.

But we can use the 3D sine waves to make something fun looking like this:

<canvas id="peace-epicycles" class="sketch" width=500 height=500></canvas>

What’s going on here?

Well, we can think of the drawing as a 3D shape because of the way it moves around in time. If you imagine the hand being drawn by a person, the three dimensions represent where the tip of their pencil is at that moment. The x and y dimensions tell us the position, and then the time dimension is the time at that moment.

<canvas id="peace-3d" class="sketch" width=500 height=500></canvas>

Now that we have a 3D pattern, we can't use the regular 2D sine waves to represent it. No matter how many of the 2D sine waves we add up, we'll never get something 3D. So we need something else.

What we can use is the 3D spiral sine waves from before. If we add up lots of those, we can get something that looks like our 3D pattern.

Remember, these waves look like circles when we look at them from front on. The name for the pattern of a circle moving around another circle is an epicycle.

<canvas id="peace-build-up" class="sketch" width=500 height=500></canvas>
<input id="peace-build-up-slider" type="range" min="0" max="1" value="1" step="any">

*Use the slider above to control how many circles there are.*

Like before, we get a pretty good approximation of our pattern with just a few circles. Because this is a fairly simple shape, all the last ones do is make the edges a little sharper.

All this applies to any drawing, really! Now it’s your chance to play around with it.

<div class="multi-container">
<div class="sketch" >
    <canvas id="draw-zone" class="sketch-child" width=500 height=500></canvas>
    <p id="draw-zone-instruction" class="instruction">Draw here!</p>
    <button id="draw-zone-undo-button" class="button embedded-button">Undo</button>
</div>
<canvas id="circle-zone" class="sketch" width=500 height=500></canvas>
</div>
<input id="circle-zone-slider" type="range" min="0" max="1" value="1" step="any">

*Use the slider to control how many circles are used for your drawing*

Again, you'll see for most shapes, we can approximate them fairly well with just a small number of circles, instead of saving all the points.

Can we use this for real data? Well, we could! In reality we have another data format called SVG, which probably does a better job for the types of shapes we tend to create. So for the moment, this is really just for making cool little gifs.

<canvas id="fourier-title" class="sketch" width=500 height=300></canvas>

There is another type of visual data that does use Fourier transforms, however.

