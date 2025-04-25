import net.sourceforge.jFuzzyLogic.FIS;
import java.util.Scanner;

public class AnimeRecommendation {
    public static void main(String[] args) {
        final String rutaArchivoFCL = "src/anime_recommendation.fcl";
        FIS sistemaDifuso = FIS.load(rutaArchivoFCL, true);

        if (sistemaDifuso == null) {
            System.err.println("No se pudo cargar el archivo FCL.");
            return;
        }

        Scanner entrada = new Scanner(System.in);
        String[] categorias = {"accion", "romance", "comedia", "drama", "fantasia", "ciencia_ficcion", "terror"};

        for (String categoria : categorias) {
            double valor = solicitarValor(entrada, categoria);
            sistemaDifuso.setVariable(categoria, valor);
        }

        sistemaDifuso.evaluate();
        double indice = sistemaDifuso.getVariable("recomendacion").getValue();

        System.out.printf("Índice de recomendación: %.2f%n", indice);
        mostrarRecomendaciones(indice);
    }

    private static double solicitarValor(Scanner sc, String genero) {
        double nivel;
        do {
            System.out.print("Ingrese nivel para " + genero + " (0 a 10): ");
            nivel = sc.nextDouble();
            if (nivel < 0 || nivel > 10) {
                System.out.println("Valor fuera de rango. Intente nuevamente.");
            }
        } while (nivel < 0 || nivel > 10);
        return nivel;
    }

    private static void mostrarRecomendaciones(double valor) {
        if (valor >= 90) {
            System.out.println("Recomendados: Attack on Titan, Sword Art Online, Steins;Gate, Fullmetal Alchemist, Code Geass.");
        } else if (valor >= 75) {
            System.out.println("Recomendados: Death Note, One Punch Man, Vinland Saga, Hunter x Hunter, Fate/Zero.");
        } else if (valor >= 60) {
            System.out.println("Recomendados: Clannad, Your Lie in April, Re:Zero, Erased, The Promised Neverland.");
        } else if (valor >= 45) {
            System.out.println("Recomendados: Tokyo Revengers, Ao Haru Ride, Noragami, Anohana, Angel Beats.");
        } else if (valor >= 30) {
            System.out.println("Recomendados: Lucky Star, Nichijou, K-On!, Saiki Kusuo no Psi-nan, Konosuba.");
        } else {
            System.out.println("Recomendados: Mirai Nikki, Another, Tokyo Ghoul, School Days, Elfen Lied.");
        }
    }
}

