# 项目架构与技术栈

## 1. 概述

本项目旨在构建一个高性能、可扩展的 AI Agent Server，作为 AI 应用开发框架，通过 A2A (Agent-to-Agent) 协议向其他 Agent Client 提供 AI 服务。我们采用混合技术栈，充分利用不同语言和工具的优势，以实现前端的快速开发、后端的高效并发处理以及 AI 核心的快速迭代。

## 2. 技术栈详情

### 2.1. 前端

*   **框架**: **Quasar**
    *   **特点**: 支持 1IN8 (一次编写，八个平台部署)，提供丰富的 UI 组件和工具，便于快速构建响应式、高性能的用户界面。
    *   **职责**: 负责用户界面的呈现、用户交互逻辑以及与后端 API 的通信。

### 2.2. 后端核心服务

*   **语言/框架**: **Golang**
    *   **特点**: 高性能、强类型、内置并发支持 (Goroutine)，编译为单文件二进制，部署轻量，启动速度快。
    *   **职责**:
        *   **API 网关**: 提供统一的外部 API 接口。
        *   **MCP (Multi-Agent Communication Protocol) 服务端**: 处理 Agent 之间的通信和协调。
        *   **A2A (Agent-to-Agent) Dispatcher**: 负责 A2A 协议消息的路由和分发。
        *   **DB 模块**: 封装数据库操作，提供统一的数据访问接口。
        *   **并发核心**: 利用 Goroutine 轻松实现高并发服务，处理大量请求和 Agent 调度。
        *   **RPC 调度 Agents**: 通过 gRPC 或其他 RPC 机制调度和管理 Python AI Agent 服务。

### 2.3. AI 核心服务

*   **语言/框架**: **Python (FastAPI)**
    *   **特点**: Python 在 AI 领域拥有丰富的库和生态系统。FastAPI 是一个现代、快速 (高性能) 的 Web 框架，基于 Starlette 和 Pydantic，易于学习和使用，支持异步编程。
    *   **职责**: 构建专门的 AI Agent Server 服务模块，专注于 AI 功能的快速迭代。
        *   **AI Agent**: 实现具体的 AI 智能体逻辑。
        *   **LLM (Large Language Model) 推理**: 集成和管理大型语言模型的推理服务。
        *   **RAG (Retrieval-Augmented Generation)**: 实现检索增强生成，结合外部知识库提升 LLM 表现。
        *   **Embedding**: 提供文本、图像等数据的 Embedding 生成服务。
        *   **工具**: 集成各种外部工具，供 AI Agent 调用。
        *   **MCP 工具链**: 实现与 Golang 后端 MCP 服务端的通信。
        *   **自动化 Workflow**: 支持复杂的 AI 工作流编排。

### 2.4. 数据存储与缓存

*   **缓存**: **Redis**
    *   **特点**: 高性能的键值存储，支持多种数据结构，可用于会话管理、消息队列、排行榜等。
    *   **职责**: 作为 Milvus/MongoDB/PostgreSQL 数据库的前端缓存，加速数据访问。在 MVP 阶段，也用作消息队列 (queue) 来处理异步任务。
*   **非结构化数据**: **MongoDB**
    *   **特点**: 文档型数据库，灵活的 Schema，适合存储非结构化或半结构化数据，如 Agent 的配置、日志、用户行为数据等。
*   **结构化数据**: **PostgreSQL**
    *   **特点**: 关系型数据库，支持 ACID 事务，数据一致性强，适合存储用户账户、订单、Agent 状态等结构化数据。
*   **向量数据**: **Milvus**
    *   **特点**: 专门为向量相似度搜索设计，支持海量向量数据的存储和查询，是 RAG 和 Embedding 服务的核心组件。

### 2.5. 数据缓存策略

*   **三级缓存**: 采用多层缓存机制，优化数据访问性能。
    1.  **SSD 集群**: 物理层面的高速存储。
    2.  **Redis Cluster**: 分布式内存缓存，提供高可用和可扩展性。
    3.  **Milvus/MongoDB/PostgreSQL 数据库自带缓存**: 数据库层面的缓存优化。

## 3. MVP (最小可行产品) 阶段技术栈

为了快速验证核心功能和用户反馈，MVP 阶段将聚焦于以下技术栈：

*   **后端**: **FastAPI + Uvicorn Workers + Redis**
    *   **FastAPI**: 快速构建 RESTful API。
    *   **Uvicorn Workers**: 提供高性能的 ASGI 服务器，支持并发处理。
    *   **Redis**: 作为消息队列处理异步任务，并作为主要的数据缓存。
*   **前端**: **Quasar**
    *   快速构建用户界面，与 FastAPI 后端进行交互。

MVP 阶段将优先实现 AI Agent 的核心功能和 A2A 协议的基本通信，逐步完善整个系统。