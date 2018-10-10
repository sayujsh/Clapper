package clapper.com.clapperapp;

import android.graphics.Bitmap;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.MultiFormatWriter;
import com.google.zxing.WriterException;
import com.google.zxing.common.BitMatrix;

public class MainActivity extends AppCompatActivity {

    int scene;
    int take;
    ImageView qrDisplay;
    Button nextScene;
    Button nextTake;
    Button prevScene;
    Button prevTake;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        qrDisplay = findViewById(R.id.qrDisplay);
        nextScene = findViewById(R.id.nextSceneButton);
        nextTake = findViewById(R.id.nextTakeButton);
        prevScene = findViewById(R.id.prevSceneButton);
        prevTake = findViewById(R.id.prevTakeButton);

        scene = 0;
        take = 0;
    }

    nextScene.setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            try {
                Bitmap bitmap = TextToImageEncode(scene + ":" + take);

                qrDisplay.setImageBitmap(bitmap);

            } catch (WriterException e) {
                e.printStackTrace();
            }

        }
    });
}
