# First Year Data Analysis

## Welcome to my First Year Data Analysis Code Repository!
There's lots to see and do in this merry land. Special thanks to the Python ```uncertainties``` package for eliminating the need for me to ever calculate uncertainties by hand, like some sort of Neanderthal. If you don't already have this package installed, or for some reason use Sypder, go to your Terminal on your respective operating system (on Windows, this is Win+R, then type ```cmd```; on Mac, this is Cmd+Space, then type ```terminal```), and type the following command:

```
pip install uncertainties
conda install uncertainties
```


### Capacitance Data Analysis
You can find this under the aptly-named ```capacitance-data-analysis.py```. You should be able to obtain plots that look something along these lines.

![scd](https://user-images.githubusercontent.com/41821907/145357108-f2b705be-6c1f-4a08-84de-578167f07469.png)
![scd-linear](https://user-images.githubusercontent.com/41821907/145357110-12a68086-97e7-495c-8839-94da9715f260.png)
![lcd](https://user-images.githubusercontent.com/41821907/145357099-98ada188-8823-4694-b834-db6e8c68ec8e.png)
![lcd-linear](https://user-images.githubusercontent.com/41821907/145357105-2f4a15ec-5e5c-4a7a-a76f-a187b0d8468d.png)

### Diffraction Data Analysis
My magnum opus. Using ```diffraction-data-analysis-b-altered.py``` contains ways you can correct the curve_fit obtained from Scipy to make it better fit the curve through applying phase shifts, vertical and horizontal scalings.

![ss-profile-a](https://user-images.githubusercontent.com/41821907/145357585-95d3f953-5098-4224-bfef-b53912d7a16f.png)
![ds-profile-b](https://user-images.githubusercontent.com/41821907/145357577-8249dc9f-843c-4a86-8c26-14b640ded473.png)
![ss-linear-a](https://user-images.githubusercontent.com/41821907/145357578-8e9d1de9-e9f5-4819-b179-43d46a16666a.png)
![ds-linear-b](https://user-images.githubusercontent.com/41821907/145357572-a0632d81-433d-4f48-a077-343be10afefc.png)
![ss-minima-b](https://user-images.githubusercontent.com/41821907/145357581-0f9e79fc-06c5-4a69-a66e-5ad2b6e48933.png)
![ds-minima-b](https://user-images.githubusercontent.com/41821907/145357576-9c3e18dd-ccf1-4e3c-9ade-6dc904d206e8.png)

### Lenses Data Analysis
Some output along these lines is expected from the file ```lenses-data-analysis.py```:
![M vs s  Python](https://user-images.githubusercontent.com/41821907/145358208-7150f2f2-fa99-4259-8496-e44403210b4e.png)


