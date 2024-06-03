from abc import ABC
from typing import List as TypingList, List
from pydantic import BaseModel, Field
import re

import logging

logger = logging.getLogger(__name__)


class MdElement(BaseModel, ABC):
    text: str
    children: List[dict] = Field(default_factory=list)

    def __repr__(self) -> str:
        return f"<{self.type}: {self.text}>"

    def __str__(self) -> str:
        return f"<{self.type}: {self.text}>"


class Header1(MdElement):

    @property
    def type(self):
        return "header1"


class Header2(MdElement):

    @property
    def type(self):
        return "header2"


class Header3(MdElement):

    @property
    def type(self):
        return "header3"


class Header4(MdElement):

    @property
    def type(self):
        return "header4"


class Header5(MdElement):

    @property
    def type(self):
        return "header5"


class Header6(MdElement):

    @property
    def type(self):
        return "header6"


class Paragraph(MdElement):

    @property
    def type(self):
        return "paragraph"


class Table(MdElement):

    @property
    def type(self):
        return "table"

    @staticmethod
    def to_json(text: str) -> dict:
        table = text.split("\n")
        headers = table[0].split("|")
        rows = [row.split("|") for row in table[2:] if row.strip()]
        return {"headers": headers, "rows": rows}


class ThematicBreak(MdElement):

    @property
    def type(self):
        return "thematic_break"


class MarkdownList(MdElement):

    @property
    def type(self):
        return "list"

    @staticmethod
    def to_list(text: str) -> TypingList[str]:
        return [item.strip() for item in text.split("\n") if item.strip()]


class CodeBlock(MdElement):

    @property
    def type(self):
        return "code_block"

    @staticmethod
    def code_type(text: str) -> str:
        if not text.startswith("```"):
            return "Unknown"
        first_line = text.split("\n")[0]
        if first_line.strip() == "```":
            return "Unknown"
        return first_line.strip("```").strip()


class BlockQuote(MdElement):

    @property
    def type(self):
        return "block_quote"


class BlockText(MdElement):

    @property
    def type(self):
        return "block_text"


class MarkdownPage(BaseModel):
    elements: TypingList[MdElement] = Field(default_factory=list)

    def add_element(self, element: MdElement):
        self.elements.append(element)

    def to_md(self) -> str:
        return merge_elements_to_md(self.elements)

    def to_elements_list(self) -> TypingList[dict]:
        return [
            {"type": ele.type, "text": ele.text, "children": ele.children}
            for ele in self.elements
        ]

    @staticmethod
    def from_md(md: str) -> "MarkdownPage":
        logger.info("Converting markdown to elements")
        elements = md_to_elements(md)
        return MarkdownPage(elements=elements)

    def toc(self, wrapped: bool = False) -> TypingList[dict]:
        toc = []
        for ele in self.elements:
            if ele.type.startswith("header"):
                if wrapped:
                    toc.append({"type": ele.type, "text": ele.text})
                else:
                    try:
                        toc.append({"type": ele.type, "text": ele.children[0]["raw"]})
                    except Exception as e:
                        logger.warning(f"Failed to get children for {ele}, {e}")
                        toc.append({"type": ele.type, "text": ele.text})
        return toc

    def __add__(self, other: "MarkdownPage") -> "MarkdownPage":
        if not isinstance(other, MarkdownPage):
            raise ValueError(f"Cannot add {type(other)} to MarkdownPage")
        return MarkdownPage(elements=self.elements + other.elements)


def format_markdown(md: str) -> str:
    """Format markdown text with mistune"""
    import mistune
    from mistune.renderers.markdown import MarkdownRenderer

    _format_markdown = mistune.create_markdown(renderer=MarkdownRenderer())
    # rewrite the thematic break
    _format_markdown.renderer.thematic_break = lambda token, state: "---\n\n"
    md = re.sub(r"\n{3,}", "\n\n", md)
    return _format_markdown(md)


def merge_elements_to_md(elements: TypingList[MdElement]) -> str:
    # merge raw
    return "\n\n".join([ele.text for ele in elements])


def md_to_elements(md: str) -> TypingList[MdElement]:
    import mistune

    markdown = mistune.create_markdown(renderer=None)

    # reformat md with mistune
    md = format_markdown(md)

    elements = []

    md_raw_blocks = md.split("\n\n")
    md_raw_blocks = [block.strip() for block in md_raw_blocks if block.strip()]

    mistune_elements: List[dict] = markdown(md)
    mistune_elements = [ele for ele in mistune_elements if ele["type"] != "blank_line"]

    for raw, element in zip(md_raw_blocks, mistune_elements):
        if not element or not element.get("type"):
            continue
        if element["type"] == "heading":
            if element["attrs"]["level"] == 1:
                elements.append(Header1(text=raw, children=element["children"]))
            elif element["attrs"]["level"] == 2:
                elements.append(Header2(text=raw, children=element["children"]))
            elif element["attrs"]["level"] == 3:
                elements.append(Header3(text=raw, children=element["children"]))
            elif element["attrs"]["level"] == 4:
                elements.append(Header4(text=raw, children=element["children"]))
            elif element["attrs"]["level"] == 5:
                elements.append(Header5(text=raw, children=element["children"]))
            elif element["attrs"]["level"] == 6:
                elements.append(Header6(text=raw, children=element["children"]))
        elif element["type"] == "paragraph":
            elements.append(Paragraph(text=raw, children=element["children"]))
        elif element["type"] == "block_code":
            elements.append(CodeBlock(text=raw))
        elif element["type"] == "list":
            elements.append(MarkdownList(text=raw, children=element["children"]))
        elif element["type"] == "block_quote":
            elements.append(BlockQuote(text=raw, children=element["children"]))
        elif element["type"] == "block_text":
            elements.append(BlockText(text=raw, children=element["children"]))
        elif element["type"] == "table":
            elements.append(Table(text=raw, children=element["children"]))
        elif element["type"] == "thematic_break":
            elements.append(ThematicBreak(text=raw))
        else:
            logger.warning(f"Unknown element type: {element['type']}")

    return elements


if __name__ == "__main__":
    md = """# Dual-channel Hybrid Neural Network for Modulation Recognition

**MIN LU<sup>1</sup>, TIANJUN PENG<sup>1,2</sup>, GUANGXUE YUE<sup>1,2</sup>, BOLIN MA<sup>2</sup>, XIANGBAI LIAO<sup>2</sup>**
1. College of Science, Jiangxi University of Science and Technology, Ganzhou, Jiangxi, 341000, China
2. College of Information Science and Engineering, Jiaxing University, Jiaxing, Zhejiang, 314001, China
*Corresponding author: Guangxue Yue (gxyue@zjxu.edu.cn)*

**ABSTRACT**
In the blind recognition of wireless communication modulation based on deep learning, how to further improve the recognition accuracy has become a key research issue. In this work, we propose a dual-channel hybrid model termed as CLDR (convolutional long short-term deep neural and residual network). The CLDR consists of the convolutional long short-term deep neural network (CLDNN) and the residual network (ResNet), where CLDNN is to reduce the variations in the spectrum and time, ResNet is to avoid gradient vanishing or exploding. In addition, we design an exponential curve decay adaptive cyclical learning rate method to decrease the training time cost of the neural network model. This method eliminates the need to experimentally search the optimal learning rate as with the fixed learning rate policy. It also avoids the slow convergence of the model due to the excessive attenuation amplitude as with the triangular learning rate policy. We test the feasibility of the CLDR model and discuss the influence of the exponential decay cyclical learning rate on the training of CLDR model based on the RadioML2016.10b public dataset. Simulation results show that the CLDR model yields a recognition accuracy of 93.1% at high SNRs, which effectively reduces the influence of external environment such as noise and fading on recognition accuracy. The training time cost of CLDR using exponential cyclical learning rate is reduced by 14.6% and 32.1% compared with triangular and fixed methods. Therefore, the exponential cyclical learning rate policy effectively reduces the training time cost of the model in the same classification accuracy.

**INDEX TERMS** Deep neural network, Residual network, Cyclical learning rate, Modulation recognition.

## I. INTRODUCTION
With the rapid development of technology such as pattern recognition and signal processing, using deep learning to classify communication modulated signals has gradually become the focus of research. Automatic modulation classification (AMC) plays an important role in wireless communication, which is widely used in military electronic warfare and commercial communications. In military communications, hostile signals need to be identified efficiently without prior information, and desired signals should be received correctly. On the other hand, for commercial communications, especially for Software Defined Radio (SDR), the AMC is essential to a wide range of communications requirements. Blind and fast recognition of received signal types is a basis of intelligent systems. AMC improves the radio spectrum utilization rate and provides the feasibility of intelligent decision for autonomous wireless spectrum monitoring system.

There are two categories of traditional AMC algorithms, the method based on likelihood estimation and the handcraft feature extraction with expert experience. In the likelihood estimation method, the modulation classification problem is represented as a multiple hypothesis testing problem. The signal is processed by the maximum likelihood estimation method or Bayesian estimation method, and the classification of modulation modes is achieved by comparing the likelihood ratio of each signal hypothesis with the threshold. Although the method based on likelihood estimation can classify modulation types well, it requires a large number of experimental samples to effectively identify the modulation type in the unknown channel, with excessive computational complexity. Traditional feature-based methods rely heavily on expert experience and perform well only in specific environments and are hard to extend to other modulation types.

Recently, deep learning is widely used in machine translation and image recognition. To build a more flexible and intelligent communication system, some scholars have studied the classification method of signal modulation types by deep learning. O'Shea et al. proposed using convolutional neural networks (CNN) to distinguish 11 different modulation types in the RadioML2016.10a dataset for the first time. And Ma K et al. used CNN network to distinguish 11 modulation types. The results show that the neural network has higher accuracy and better flexibility in distinguishing different modulation types than the feature-based methods. However, CNN has the problem of gradient vanishing or exploding. The performance of the model will decrease when it reaches a certain depth. Kaiming and Gao Huang et al introduced ResNet and DenseNet to avoid gradient vanishing or exploding problem, and the feature mapping is strengthened by creating shortcut paths between different convolution layers. The ResNet architecture and DenseNet architecture successfully distinguished 10 different modulation types in RadioML2016.10b dataset. Recently, the construction of hybrid neural network to distinguish modulation types has become a focus of study. Sainath et al. took advantage of the complementarity of long and short-term memory networks (LSTM), CNN and deep neural networks (DNNs), combining them into a unified network architecture, which is termed as CLDNN. The same network structure is introduced into automatic modulation recognition. The CLDNN is used to classify the 10 different modulation types in RadioML2016.10b dataset. However, the neural network will fall into the saddle point in the process of training, resulting in slow convergence speed and increased training time costs.

In order to avoid the model training falling into the saddle point and reduce the time cost of network training, the adjustment of super-parameters becomes crucial to the training of the neural network. Choosing the right learning rate is a challenging task. If the learning rate is too low, it may lead to a very slow training process and slow down the convergence speed of the neural network. However, setting a too high learning rate may cause deviation from the optimal point, and the network cannot reach convergence. In addition, choosing a reasonable learning rate requires multiple experiments. Cyclical learning rate is an effective learning rate adjustment policy that can accelerate the convergence rate and reduce the training time cost of the neural network model.

The contribution of this paper is thus twofold. Firstly, we design an exponential cyclical learning rate method. In this method, the learning rate is adjusted by using linear scaling with an exponential decay trend, which contributes to achieving faster convergence speed and lower training time cost of the model. Secondly, we propose a dual-channel hybrid neural network model termed as CLDR, which creatively combines the complimentary merits of CLDNN and ResNet network architectures. It improves the recognition accuracy of different modulation types under high SNRs.

## II. NETWORK ARCHITECTURE MODEL AND LEARNING RATE POLICY
### A. NETWORK ARCHITECTURE MODEL
In this paper, we propose a hybrid network model, as shown in Figure 1. The network architecture is a parallel dual-path network of CLDNN and ResNet. In the branch of CLDNN network, we use three convolution layers to extract the features of I/Q signals to reduce the spectrum variation, and then use the time correlation of LSTM to reduce the time variation. In addition, in order to reduce the feature dimension, we introduce a linear layer between the first convolutional layer and the third convolutional layer of CLDNN. Each convolutional layer uses a filter size of 1 × 3 and an LSTM with 50 hidden units in the CLDNN. In another branch, we introduce ResNet architecture to avoid gradient vanishing or exploding. In our network, The ResNet consists of three residual stacks, each residual stack contains a convolutional layer, two residual units, and a maximum pooling layer. Moreover, we add a batch-normalized layer behind each convolution layer to prevent overfitting. The filter size of the convolutional layer is 1 × 5. The extracted features are divided into 10 classes through the fully connected layers with 128 and 10 neurons. We validate the performance of the CLDR model through the recognition accuracy under different SNRs, loss rate, and confusion matrix.

### B. LEARNING RATE POLICY
The learning rate is an important hyperparameter for neural network training, which determines how much error is needed to update the weights. For different optimizers, the network model converges slowly when the learning rate is set too small. Moreover, if the learning rate value is set too large, oscillations will occur near the extreme points, and the network will fail to converge. In addition, choosing a reasonable learning rate requires multiple experiments. Cyclical learning rate is an effective learning rate adjustment policy that can accelerate the convergence speed of network training and reduce the time cost of network training. The specific adjustment process consists of two steps: determining the range of learning rate cycle change and the step size of the learning rate adjustment in this range. In this paper, we have adopted the fixed learning rate policy, triangular cyclical learning rate policy, and exponential cyclical learning rate policy to train the network model.

#### 1) Fixed learning rate policy
In the fixed learning rate policy, we set the learning rate of the model as a fixed value. However, in order to find the best learning rate value, it requires a large number of experiments to manually change the learning rate. We introduce an efficient and simple Adam optimization method to avoid additional computation. The simulation results in [23] shows that the Adam optimizer has good performance when the learning rate value is 0.001. The weights of the model are updated by the following formula:

```text
(2) α = 0.001
(3) ˆmt = β1 · mt−1 + (1 − β1) · gt
(4) ˆνt = β2 · νt−1 + (1 − β2) · gt^2
(5) mt = ˆmt / (1 − β1^t)
(6) νt = ˆνt / (1 − β2^t)
```

where α is the learning rate, ˆmt is the bias-corrected first-order moment estimate, ˆνt is the bias-corrected second original moment estimate, mt is the biased first-order moment estimate, νt is the biased second original moment estimate, gt is the gradient, β1 , β2 are the exponential decay rates for the moment estimates, and β1 = 0.9, β2 = 0.999, ft is the stochastic objective function. ε represents a constant, and ε = 1e−8.

#### 2) Triangular cyclical learning rate policy
In order to eliminate the search for the best learning rate by means of multiple experiments, L. N. Smith et al. proposed the method of triangular cyclical learning rate. Triangular cyclical learning rate policy is a triangle update method. The learning rate cyclically changes between the minimum and maximum, and the maximum value decays in half at the end of each cycle, as shown in Figure 2. The learning rate changes linearly and periodically between the maximum and minimum values. The learning rate is updated every time a batch is passed during training. The updated specific value is as follows [24]:

```
(7) c = f1(1 + b2 · s)
```

---

- c is the learning rate at the current iteration.
    - f1 is the initial learning rate.
        - a1 is the maximum learning rate.
    - b1 is the base learning rate.
- f1 is the initial learning rate.
- b1 is the base learning rate.

![Figure 2: Triangular cyclical learning rate policy](https://jing10.top/wp-content/uploads/2021/07/fig2.png)

[Link](https://jing10.top/wp-content/uploads/2021/07/fig2.png)

### III. RESULTS
We tested the feasibility of the CLDR model and discussed the influence of the exponential decay cyclical learning rate on the training of the CLDR model based on the RadioML2016.10b public dataset. Simulation results showed that the CLDR model yielded a recognition accuracy of 93.1% at high SNRs, which effectively reduced the influence of external environment such as noise and fading on recognition accuracy. The training time cost of CLDR using exponential cyclical learning rate was reduced by 14.6% and 32.1% compared with triangular and fixed methods. Therefore, the exponential cyclical learning rate policy effectively reduced the training time cost of the model while maintaining the same classification accuracy.

- c is the learning rate at the current iteration.
- f1 is the initial learning rate.
- b1 is the base learning rate.

> This is block_quote

| Header1 | Header2 | Header3 |
| --- | --- | --- |
| 1 | 2 | 3 |
| 4 | 5 | 6 |
| 7 | 8 | 9 |

---

This is the end

"""
    import json

    md_page = MarkdownPage.from_md(md)
    toc = md_page.toc(wrapped=False)
    print(json.dumps(toc, indent=4))

    # import mistune
    # from mistune import create_markdown

    # from mistune.toc import add_toc_hook, render_toc_ul
    # markdown = mistune.create_markdown(renderer=None)
    # md_new: List = mistune.markdown(md, escape=False, renderer=None)
    # markdown_render = mistune.create_markdown(renderer=None)
    # add_toc_hook(markdown_render)
    # markdown_render = create_markdown(
    #     escape=False,
    #     hard_wrap=True,
    #     renderer=None,
    #     # plugins=['strikethrough', 'footnotes', 'table', 'speedup']
    # )
    # md_new: List = markdown_render(md)

    # markdown_elements = md_to_elements(md)
    # for ele in markdown_elements:
    #     print("=" * 80)
    #     print(ele)

    # # merge
    # new_md = merge_elements_to_md(markdown_elements)
    # print(new_md)

    # for ele in md_new:
    #     if ele["type"] == "blank_line":
    #         continue
    #     print("=" * 80)
    #     print(ele)
    # render to markdown but not a list
    # print(markdown_render(ele))

    # md_new = [i for i in md_new if i["type"] != "blank_line"]
    # save to "md_new.json"
    # import json

    # with open("md_new.json", "w") as f:
    #     json.dump(md_new, f, indent=4)
