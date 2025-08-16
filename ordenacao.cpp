#include <iostream>     
#include <fstream>      
#include <cstdlib>      
#include <ctime>        
#include <cstring>      

using namespace std;

#define NUM_EXECUCOES 30

//  Merge Sort
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    int* L = new int[n1];
    int* R = new int[n2];

    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];

    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];

    delete[] L;
    delete[] R;
}

void mergesort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergesort(arr, l, m);
        mergesort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

//  Quick Sort
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quicksort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

// Função Auxiliar
void gerar_lista(int arr[], int n, const char* tipo) {
    if (strcmp(tipo, "crescente") == 0) {
        for (int i = 0; i < n; i++) arr[i] = i;
    } else if (strcmp(tipo, "decrescente") == 0) {
        for (int i = 0; i < n; i++) arr[i] = n - i;
    } else {
        for (int i = 0; i < n; i++) arr[i] = rand() % 10000;
    }
}

void copiar_lista(int origem[], int destino[], int n) {
    for (int i = 0; i < n; i++) destino[i] = origem[i];
}

void salvar_resultado(const char* nome_arquivo, double tempos[]) {
    ofstream f(nome_arquivo);
    if (!f.is_open()) {
        cout << "Erro ao abrir arquivo " << nome_arquivo << endl;
        return;
    }
    for (int i = 0; i < NUM_EXECUCOES; i++) {
        f << tempos[i] << endl;
    }
    f.close();
}

// Função principal
int main() {
    srand(time(NULL)); // Inicializa gerador de números aleatórios

    int tamanhos[] = {100, 1000, 2000, 3000, 4000, 5000, 10000};
    const char* tipos[] = {"crescente", "decrescente", "aleatoria"};

    for (int t = 0; t < 3; t++) {
        for (int i = 0; i < 7; i++) {
            int n = tamanhos[i];
            int* lista_original = new int[n];
            int* lista_copia = new int[n];
            double tempos_merge[NUM_EXECUCOES];
            double tempos_quick[NUM_EXECUCOES];

            cout << "\nTestando tipo: " << tipos[t] << ", tamanho: " << n << endl;
            gerar_lista(lista_original, n, tipos[t]);

            // Exibir amostra da lista gerada
            if (n >= 10) {
                cout << "Exemplo de lista " << tipos[t] << ": ";
                for (int k = 0; k < 10; k++) {
                    cout << lista_original[k] << " ";
                }
                cout << "...\n";
            }

            for (int j = 0; j < NUM_EXECUCOES; j++) {
                // Mergesort
                copiar_lista(lista_original, lista_copia, n);
                clock_t start = clock();
                mergesort(lista_copia, 0, n - 1);
                clock_t end = clock();
                tempos_merge[j] = double(end - start) / CLOCKS_PER_SEC;

                // Quicksort
                copiar_lista(lista_original, lista_copia, n);
                start = clock();
                quicksort(lista_copia, 0, n - 1);
                end = clock();
                tempos_quick[j] = double(end - start) / CLOCKS_PER_SEC;
            }

            // Salvar resultados
            char nome_arquivo[100];
            sprintf(nome_arquivo, "saida_mergesort_%s_%d.txt", tipos[t], n);
            salvar_resultado(nome_arquivo, tempos_merge);

            sprintf(nome_arquivo, "saida_quicksort_%s_%d.txt", tipos[t], n);
            salvar_resultado(nome_arquivo, tempos_quick);

            delete[] lista_original;
            delete[] lista_copia;
        }
    }

    cout << "\nTodos os testes foram concluidos com sucesso!" << endl;
    return 0;
}
